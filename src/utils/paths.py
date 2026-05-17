from pathlib import Path
from src import config

REQUIRED_DIRS = [
    config.RAW, config.INTERIM, config.PROCESSED, config.ANALYTICS, config.POWERBI,
    config.FIGURES, config.METRICS, config.PREDICTIONS, config.REPORTS, config.MODELS,
    config.DOCS, config.SQL_OUT,
]

def ensure_dirs() -> None:
    for path in REQUIRED_DIRS:
        Path(path).mkdir(parents=True, exist_ok=True)
