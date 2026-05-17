from __future__ import annotations
import pandas as pd

def country_capacity(reactors: pd.DataFrame) -> pd.DataFrame:
    return reactors[reactors["status_group"].eq("Operating")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
