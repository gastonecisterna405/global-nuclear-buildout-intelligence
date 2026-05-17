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

def step(i: int, msg: str) -> None:
    print(f"[{i}/21] {msg}", flush=True)

def main() -> None:
    step(1, "Initializing folders...")
    ensure_dirs()
    step(2, "Registering data sources...")
    register_sources()
    step(3, "Ingesting available data sources...")
    try:
        ingest_owid()
        ingest_world_bank()
    except Exception as exc:
        print(f"Warning: optional download failed and pipeline will continue: {exc}")
    step(4, "Generating manual ingestion templates...")
    create_manual_templates()
    create_dirty_sample_data()
    step(5, "Cleaning source datasets...")
    step(6, "Integrating reactor master table...")
    reactors, countries, pipeline, taxonomy, scenarios = integrate_all()
    step(7, "Integrating country profile table...")
    step(8, "Building technology taxonomy...")
    step(9, "Running data quality checks...")
    run_data_quality_checks(reactors, countries)
    step(10, "Running full EDA...")
    docs, topics = run_nlp_pipeline()
    generate_eda_outputs(reactors, countries, pipeline, taxonomy, scenarios, topics)
    step(11, "Building forecasting features...")
    step(12, "Training forecasting models...")
    forecasts, forecast_metrics = train_capacity_forecaster(countries)
    run_statsmodels_global_forecast(reactors)
    step(13, "Building project risk scoring...")
    risk, risk_metrics = train_project_realization_models(pipeline)
    step(14, "Building technology maturity scoring...")
    score_technology_maturity(taxonomy)
    step(15, "Running country clustering...")
    cluster_countries(countries)
    step(16, "Running electricity supply scenarios...")
    # Scenario table was generated during integration and exported to predictions.
    step(17, "Running NLP pipeline...")
    # NLP was run before EDA so figures can use topic outputs.
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
    print("Pipeline complete. Run: streamlit run src/dashboard/app.py")

if __name__ == "__main__":
    main()
