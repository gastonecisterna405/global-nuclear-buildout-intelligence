from __future__ import annotations
import pandas as pd
from src import config

def export_powerbi_tables() -> list[str]:
    config.POWERBI.mkdir(parents=True, exist_ok=True)
    mapping = {
        "fact_reactors.csv": config.PROCESSED / "reactors_master.csv",
        "fact_reactor_pipeline.csv": config.PROCESSED / "reactor_pipeline.csv",
        "fact_capacity_scenarios.csv": config.PROCESSED / "nuclear_capacity_scenarios.csv",
        "fact_forecasts.csv": config.PREDICTIONS / "capacity_forecasts.csv",
        "fact_project_risk_scores.csv": config.PREDICTIONS / "project_risk_scores.csv",
        "fact_technology_maturity.csv": config.PREDICTIONS / "technology_maturity_scores.csv",
        "fact_nlp_policy_signals.csv": config.PROCESSED / "nlp_policy_documents.csv",
        "model_metrics.csv": config.PROCESSED / "model_metrics.csv",
    }
    written = []
    for out, src in mapping.items():
        if src.exists():
            df = pd.read_csv(src)
            df.to_csv(config.POWERBI / out, index=False)
            written.append(out)
    countries = pd.read_csv(config.PROCESSED / "country_nuclear_profile.csv")
    countries.to_csv(config.POWERBI / "dim_country.csv", index=False)
    countries[["region"]].drop_duplicates().to_csv(config.POWERBI / "dim_region.csv", index=False)
    pd.read_csv(config.PROCESSED / "technology_taxonomy.csv").to_csv(config.POWERBI / "dim_technology.csv", index=False)
    pd.DataFrame({"year": range(1950, 2051), "decade": [(y//10)*10 for y in range(1950, 2051)]}).to_csv(config.POWERBI / "dim_date.csv", index=False)
    return written
