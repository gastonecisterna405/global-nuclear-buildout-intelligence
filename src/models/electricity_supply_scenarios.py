from __future__ import annotations
import pandas as pd

def estimate_generation_twh(capacity_gw: float, capacity_factor: float) -> float:
    return capacity_gw * capacity_factor * 8.76

def add_value_proxy(df: pd.DataFrame, price_per_mwh: float = 75.0) -> pd.DataFrame:
    out = df.copy()
    out["estimated_mwh"] = out["estimated_generation_twh"] * 1_000_000
    out["price_per_mwh"] = price_per_mwh
    out["estimated_market_value_usd"] = out["estimated_mwh"] * price_per_mwh
    return out
