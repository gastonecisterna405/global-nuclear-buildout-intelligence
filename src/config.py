from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
ANALYTICS = DATA / "analytics"
POWERBI = DATA / "powerbi"
OUTPUTS = ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
METRICS = OUTPUTS / "metrics"
PREDICTIONS = OUTPUTS / "predictions"
REPORTS = OUTPUTS / "reports"
MODELS = ROOT / "models"
DOCS = ROOT / "docs"
SQL_OUT = OUTPUTS / "tables" / "sql_query_results"
CURRENT_YEAR = 2026
