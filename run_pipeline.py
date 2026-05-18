from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.paths import ensure_dirs
from src.data.source_registry import register_sources
from src.data.manual_ingestion_templates import create_manual_templates
from src.data.sample_data import create_dirty_sample_data
from src.data.ingest_owid_ember import ingest_owid
from src.data.ingest_world_bank import ingest_world_bank
from src.data.integrate_sources import integrate_all
from src.data.data_quality_checks import run_data_quality_checks
from src.nlp.policy_signal_scoring import run_nlp_pipeline
from src.eda.eda_report_generator import generate_eda_outputs
from src.features.panel_features import build_panel_dataset, build_project_completion_dataset
from src.models.nuclear_generation_forecast import train_nuclear_generation_forecast
from src.models.project_completion_classifier import train_project_completion_classifier
from src.models.capacity_forecasting_xgboost import train_capacity_forecaster
from src.models.capacity_forecasting_statsmodels import run_statsmodels_global_forecast
from src.models.project_realization_classifier import train_project_realization_models
from src.models.technology_maturity_score import score_technology_maturity
from src.models.country_clustering import cluster_countries
from src.models.model_evaluation import write_model_metrics_table
from src.sql.build_database import build_sqlite_database
from src.sql.run_queries import run_sql_queries
from src.sql.export_powerbi_tables import export_powerbi_tables
from src.reports.generate_executive_report import generate_executive_report
from src.reports.generate_model_card import generate_model_card
from src.reports.generate_interview_brief import generate_interview_brief

N_STEPS = 23

def step(i: int, msg: str) -> None:
    print(f"[{i}/{N_STEPS}] {msg}", flush=True)

def main() -> None:
    step(1,  "Initializing folders...")
    ensure_dirs()

    step(2,  "Registering data sources...")
    register_sources()

    step(3,  "Ingesting available data sources...")
    owid = None
    try:
        owid = ingest_owid()
        ingest_world_bank()
    except Exception as exc:
        print(f"  Warning: optional download failed — pipeline will continue: {exc}")

    step(4,  "Generating manual ingestion templates...")
    create_manual_templates()
    create_dirty_sample_data()

    step(5,  "Cleaning source datasets...")
    step(6,  "Integrating reactor master table...")
    reactors, countries, pipeline, taxonomy, scenarios = integrate_all()

    step(7,  "Running data quality checks...")
    run_data_quality_checks(reactors, countries)

    step(8,  "Running NLP pipeline...")
    docs, topics = run_nlp_pipeline()

    step(9,  "Running EDA outputs...")
    generate_eda_outputs(reactors, countries, pipeline, taxonomy, scenarios, topics)

    # ── Real predictive models (OWID panel data) ──────────────────────────────
    step(10, "Building panel dataset from OWID energy data...")
    panel_df = None
    project_completion_df = None

    if owid is not None and not owid.empty:
        try:
            panel_df = build_panel_dataset(owid)
            print(f"  Panel dataset: {len(panel_df)} rows, "
                  f"{panel_df.country.nunique()} countries, "
                  f"{panel_df.year.min()}–{panel_df.year.max()}")
        except Exception as exc:
            print(f"  Warning: panel dataset failed: {exc}")
    else:
        print("  OWID data not available — skipping panel model.")

    step(11, "Building project completion dataset from reactor history...")
    try:
        project_completion_df = build_project_completion_dataset(reactors)
        n_pos = (project_completion_df.completed_on_time == 1).sum()
        n_neg = (project_completion_df.completed_on_time == 0).sum()
        print(f"  Project completion dataset: {len(project_completion_df)} labeled projects "
              f"({n_pos} on-time, {n_neg} delayed/at-risk)")
    except Exception as exc:
        print(f"  Warning: project completion dataset failed: {exc}")

    step(12, "Training nuclear generation forecast (panel, temporal CV)...")
    share_forecast_metrics = {}
    if panel_df is not None and len(panel_df) >= 50:
        try:
            _, share_forecast_metrics = train_nuclear_generation_forecast(panel_df)
            best = share_forecast_metrics.get("best_model", "?")
            mae  = share_forecast_metrics["models"][best]["test_mae"]
            r2   = share_forecast_metrics["models"][best].get("test_r2", "?")
            skill = share_forecast_metrics["models"][best].get("skill_vs_mean", "?")
            print(f"  Best model: {best} | Test MAE: {mae:.2f}pp | R²: {r2} | "
                  f"Skill vs mean: {skill}")
        except Exception as exc:
            print(f"  Warning: nuclear share forecast failed: {exc}")
    else:
        print("  Insufficient panel data — skipping.")

    step(13, "Training project completion classifier (real labels)...")
    completion_metrics = {}
    if project_completion_df is not None and len(project_completion_df) >= 20:
        try:
            _, completion_metrics = train_project_completion_classifier(project_completion_df)
            best = completion_metrics.get("best_model", "?")
            cv_f1 = completion_metrics["models"][best]["cv_f1"]
            auc   = completion_metrics["models"][best].get("roc_auc", "?")
            print(f"  Best model: {best} | CV F1: {cv_f1:.3f} | ROC-AUC: {auc}")
        except Exception as exc:
            print(f"  Warning: completion classifier failed: {exc}")
    else:
        print("  Insufficient labeled data — skipping.")

    # ── Legacy demo models (kept for pipeline comparison) ─────────────────────
    step(14, "Training capacity forecasting model (cross-sectional, demo)...")
    forecasts, forecast_metrics = train_capacity_forecaster(countries)
    run_statsmodels_global_forecast(reactors)

    step(15, "Training project risk scoring (heuristic, demo)...")
    risk, risk_metrics = train_project_realization_models(pipeline)

    step(16, "Scoring technology maturity...")
    score_technology_maturity(taxonomy)

    step(17, "Running country clustering...")
    cluster_countries(countries)

    step(18, "Building SQLite database...")
    write_model_metrics_table(forecast_metrics, risk_metrics)
    build_sqlite_database()
    run_sql_queries()

    step(19, "Exporting Power BI tables...")
    export_powerbi_tables()

    step(20, "Generating executive report...")
    generate_executive_report()
    generate_model_card()

    step(21, "Generating interview brief...")
    generate_interview_brief()

    step(22, "Done.")
    print("\nPipeline complete.")
    print("Real models trained:")
    if share_forecast_metrics:
        best = share_forecast_metrics.get("best_model","?")
        print(f"  nuclear_share_forecast → {best} "
              f"(test MAE: {share_forecast_metrics['models'][best]['test_mae']:.2f}pp, "
              f"target: nuclear share in 5 years, temporal CV)")
    if completion_metrics:
        best = completion_metrics.get("best_model","?")
        print(f"  project_completion_classifier → {best} "
              f"(CV F1: {completion_metrics['models'][best]['cv_f1']:.3f}, "
              f"target: completes in ≤10 years, real labels)")
    print("\nRun: streamlit run src/dashboard/app.py")

if __name__ == "__main__":
    main()
