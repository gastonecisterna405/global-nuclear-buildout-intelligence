from __future__ import annotations
import sqlite3
import pandas as pd
from src import config

TABLES = {
    "reactors": "reactors_master.csv",
    "countries": "country_nuclear_profile.csv",
    "technologies": "technology_taxonomy.csv",
    "pipeline_projects": "reactor_pipeline.csv",
    "capacity_scenarios": "nuclear_capacity_scenarios.csv",
    "model_metrics": "model_metrics.csv",
    "data_sources": "data_sources.csv",
    "policy_documents": "nlp_policy_documents.csv",
}

def build_sqlite_database() -> str:
    db = config.OUTPUTS / "nuclear_buildout.sqlite"
    with sqlite3.connect(db) as conn:
        for table, file in TABLES.items():
            path = config.PROCESSED / file
            if path.exists():
                pd.read_csv(path).to_sql(table, conn, if_exists="replace", index=False)
        for table, path in {
            "forecasts": config.PREDICTIONS / "capacity_forecasts.csv",
            "project_risk_scores": config.PREDICTIONS / "project_risk_scores.csv",
            "technology_maturity_scores": config.PREDICTIONS / "technology_maturity_scores.csv",
            "nlp_topics": config.ANALYTICS / "topic_distribution.csv",
        }.items():
            if path.exists():
                pd.read_csv(path).to_sql(table, conn, if_exists="replace", index=False)
    return str(db)
