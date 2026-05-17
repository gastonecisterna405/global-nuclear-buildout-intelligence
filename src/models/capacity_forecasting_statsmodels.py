from __future__ import annotations

import warnings

import pandas as pd
from src import config


def run_statsmodels_global_forecast(reactors: pd.DataFrame) -> pd.DataFrame:
    operating = reactors[reactors["commercial_operation_date"].notna()].copy()
    operating["year"] = pd.to_datetime(operating["commercial_operation_date"]).dt.year

    annual_int = operating.groupby("year")["capacity_mwe"].sum().sort_index().cumsum()

    # Fill gaps so the series has a proper annual frequency for statsmodels.
    full_range = range(int(annual_int.index.min()), int(annual_int.index.max()) + 1)
    annual_int = annual_int.reindex(full_range).ffill()
    annual = annual_int.copy()
    annual.index = pd.date_range(
        start=str(int(annual_int.index[0])), periods=len(annual_int), freq="YE"
    )

    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        if len(annual) < 4:
            raise ValueError("Not enough annual observations")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ExponentialSmoothing(annual, trend="add", seasonal=None).fit()
            fc = model.forecast(10)
        last_year = int(annual_int.index[-1])
        forecast_years = list(range(last_year + 1, last_year + 11))
        fc_values = fc.values.tolist()
    except Exception:
        last = float(annual_int.iloc[-1]) if len(annual_int) else 0.0
        avg = float(annual_int.diff().dropna().tail(5).mean()) if len(annual_int) > 1 else 1000.0
        forecast_years = list(range(2027, 2037))
        fc_values = [last + (i + 1) * avg for i in range(10)]

    out = pd.DataFrame({
        "year": forecast_years,
        "global_capacity_mwe_forecast": fc_values,
    })
    out.to_csv(config.PREDICTIONS / "statsmodels_global_capacity_forecast.csv", index=False)
    return out
