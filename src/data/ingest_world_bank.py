from __future__ import annotations

import pandas as pd
import requests
from src import config

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "SP.POP.TOTL": "population",
    "NY.GDP.PCAP.CD": "gdp_per_capita",
}

def ingest_world_bank(countries: list[str] | None = None, timeout: int = 20) -> pd.DataFrame:
    countries = countries or ["US", "CN", "RU", "IN", "FR", "GB", "KR", "JP", "CA", "AE", "TR", "EG", "PL", "BD", "AR", "BR"]
    frames = []
    for code in countries:
        for indicator, name in INDICATORS.items():
            url = f"https://api.worldbank.org/v2/country/{code}/indicator/{indicator}?format=json&per_page=70"
            try:
                data = requests.get(url, timeout=timeout).json()
                rows = data[1] if isinstance(data, list) and len(data) > 1 else []
                for row in rows:
                    if row.get("value") is not None:
                        frames.append({"iso2": code, "country": row["country"]["value"], "year": int(row["date"]), "indicator": name, "value": row["value"]})
            except Exception:
                continue
    df = pd.DataFrame(frames)
    out = config.RAW / "world_bank" / "world_bank_wdi_long.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not df.empty:
        df.to_csv(out, index=False)
    else:
        (config.RAW / "world_bank" / "DOWNLOAD_FAILED.txt").write_text("World Bank download failed; pipeline will use sample data.\n", encoding="utf-8")
    return df
