from __future__ import annotations

import pandas as pd
import requests
from src import config

OWID_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

def ingest_owid(timeout: int = 20) -> pd.DataFrame:
    out = config.RAW / "our_world_in_data" / "owid_energy_data.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(OWID_URL, timeout=timeout)
        r.raise_for_status()
        out.write_bytes(r.content)
        return pd.read_csv(out)
    except Exception as exc:
        marker = config.RAW / "our_world_in_data" / "DOWNLOAD_FAILED.txt"
        marker.write_text(f"OWID download failed; pipeline will use sample data. Reason: {exc}\n", encoding="utf-8")
        return pd.DataFrame()
