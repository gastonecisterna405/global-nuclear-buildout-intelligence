from __future__ import annotations
import pandas as pd
from src import config

def ingest() -> pd.DataFrame:
    """Adapter skeleton for IAEA SMR Catalogue.

    This source is documented for manual ingestion because reliable bulk
    programmatic access may require interactive exports, PDFs, or API keys.
    See docs/data_sources_inventory.md and data/raw templates.
    """
    marker = config.RAW / "iaea_smr" / "MANUAL_INGESTION_REQUIRED.txt"
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("IAEA SMR Catalogue requires manual/public export review for this portfolio build.\n", encoding="utf-8")
    return pd.DataFrame()
