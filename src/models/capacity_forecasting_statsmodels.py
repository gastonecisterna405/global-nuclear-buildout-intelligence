from __future__ import annotations
import json
import pandas as pd
from src import config

def run_statsmodels_global_forecast(reactors: pd.DataFrame) -> pd.DataFrame:
    rows = []
    operating = reactors[reactors["commercial_operation_date"].notna()].copy()
    operating["year"] = pd.to_datetime(operating["commercial_operation_date"]).dt.year
    annual = operating.groupby("year")["capacity_mwe"].sum().sort_index().cumsum()
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        if len(annual) >= 4:
            model = ExponentialSmoothing(annual, trend="add", seasonal=None).fit()
            fc = model.forecast(10)
        else:
            raise ValueError("Not enough annual observations")
    except Exception:
        last = annual.iloc[-1] if len(annual) else 0
        avg = annual.diff().dropna().tail(5).mean() if len(annual) > 1 else 1000
        fc = pd.Series({y: last + (i + 1) * avg for i, y in enumerate(range(2027, 2037))})
    out = pd.DataFrame({"year": fc.index.astype(int), "global_capacity_mwe_forecast": fc.values})
    out.to_csv(config.PREDICTIONS / "statsmodels_global_capacity_forecast.csv", index=False)
    return out
