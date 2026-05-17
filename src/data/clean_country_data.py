from __future__ import annotations

import pandas as pd
from src import config

def clean_country_context() -> pd.DataFrame:
    df = pd.read_csv(config.RAW / "sample" / "dirty_country_context_raw.csv")
    df["nuclear_generation_twh"] = df["electricity_generation_twh"] * df["nuclear_share_fraction"]
    df["nuclear_share_percent"] = df["nuclear_share_fraction"] * 100
    out = df.drop(columns=["nuclear_share_fraction"])
    out.to_csv(config.INTERIM / "country_context.csv", index=False)
    return out
