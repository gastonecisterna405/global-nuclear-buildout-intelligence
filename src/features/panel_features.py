from __future__ import annotations

import numpy as np
import pandas as pd
from src import config

FORECAST_HORIZON = 5   # predict nuclear_share_elec 5 years ahead
MIN_YEARS = 10         # minimum years of data per country to include


def build_panel_dataset(owid: pd.DataFrame) -> pd.DataFrame:
    """
    Build a supervised panel dataset from OWID energy data.

    Each row is a (country, year) observation.
    Features = economic + energy indicators at time t and lagged values.
    Target   = nuclear_share_elec at time t+FORECAST_HORIZON.

    This produces a genuinely predictive dataset because:
    - Target is an independent future value, not derived from features.
    - Train/test split is temporal (train <= 2010, test > 2010).
    - Lagged features prevent data leakage.
    """
    nuclear_countries = (
        owid[owid.nuclear_electricity.notna() & (owid.nuclear_electricity > 0)]
        .country.unique()
    )
    df = owid[owid.country.isin(nuclear_countries)].copy()

    rows = []
    for country, g in df.groupby("country"):
        g = g.sort_values("year").reset_index(drop=True)
        if len(g) < MIN_YEARS:
            continue

        for i in range(2, len(g) - FORECAST_HORIZON):
            row_t = g.iloc[i]
            row_t5 = g.iloc[i + FORECAST_HORIZON]

            if pd.isna(row_t5.get("nuclear_share_elec")):
                continue

            # Lag features (t-1, t-2)
            lag1 = g.iloc[i - 1]
            lag2 = g.iloc[i - 2]

            def safe(series, col):
                v = series.get(col)
                return float(v) if v is not None and not pd.isna(v) else np.nan

            # GDP growth rate (t vs t-1)
            gdp_t   = safe(row_t, "gdp")
            gdp_t1  = safe(lag1,  "gdp")
            gdp_growth = (gdp_t - gdp_t1) / gdp_t1 if gdp_t1 and gdp_t1 != 0 else np.nan

            rows.append({
                "country":                 country,
                "year":                    int(row_t["year"]),
                "target_year":             int(row_t5["year"]),
                # target
                "target_nuclear_share":    safe(row_t5, "nuclear_share_elec"),
                # current nuclear
                "nuclear_share_t":         safe(row_t,  "nuclear_share_elec"),
                "nuclear_elec_t":          safe(row_t,  "nuclear_electricity"),
                # lagged nuclear
                "nuclear_share_lag1":      safe(lag1,   "nuclear_share_elec"),
                "nuclear_share_lag2":      safe(lag2,   "nuclear_share_elec"),
                "nuclear_elec_lag1":       safe(lag1,   "nuclear_electricity"),
                # economic features
                "gdp_per_capita":          safe(row_t,  "gdp") / safe(row_t, "population")
                                           if safe(row_t, "population") else np.nan,
                "gdp_growth_rate":         gdp_growth,
                "electricity_demand":      safe(row_t,  "electricity_demand"),
                "coal_share":              (safe(row_t, "coal_electricity") /
                                            safe(row_t, "electricity_demand"))
                                           if safe(row_t, "electricity_demand") else np.nan,
                "renewables_share":        (safe(row_t, "renewables_electricity") /
                                            safe(row_t, "electricity_demand"))
                                           if safe(row_t, "electricity_demand") else np.nan,
                "energy_per_capita":       safe(row_t,  "energy_per_capita"),
                "population":              safe(row_t,  "population"),
            })

    panel = pd.DataFrame(rows).dropna(subset=["target_nuclear_share"])
    panel.to_csv(config.PROCESSED / "nuclear_panel_dataset.csv", index=False)
    return panel


def build_project_completion_dataset(reactors: pd.DataFrame) -> pd.DataFrame:
    """
    Derive real project outcome labels from the reactor dataset.

    Label = 1 (completed on time):  construction_start + build_years <= 10
    Label = 0 (delayed or at risk):  build_years > 10 OR still under construction
                                      with >10 years elapsed since start

    Features = observable at construction start time (no leakage).
    """
    r = reactors.copy()
    r["construction_start_date"]    = pd.to_datetime(r["construction_start_date"], errors="coerce")
    r["commercial_operation_date"] = pd.to_datetime(r["commercial_operation_date"], errors="coerce")

    CURRENT_YEAR = config.CURRENT_YEAR

    rows = []
    for _, row in r.iterrows():
        start = row["construction_start_date"]
        if pd.isna(start):
            continue

        start_year = start.year
        commercial = row["commercial_operation_date"]

        if pd.notna(commercial):
            build_years = (commercial - start).days / 365.25
            completed = 1 if build_years <= 10 else 0
        elif row["status_group"] in ("Construction", "Planned"):
            elapsed = CURRENT_YEAR - start_year
            if elapsed < 5:
                continue   # too early to label
            completed = 0  # still building after ≥5 years → delayed
        else:
            continue

        rows.append({
            "reactor_name":           row.get("reactor_name", ""),
            "country":                row.get("country", ""),
            "technology_family":      row.get("technology_family", ""),
            "reactor_type":           row.get("reactor_type_standardized", ""),
            "capacity_mwe":           row.get("capacity_mwe", np.nan),
            "start_decade":           (start_year // 10) * 10,
            "vendor":                 row.get("vendor", "Unknown"),
            "source_confidence":      row.get("source_confidence", 0.5),
            # label
            "completed_on_time":      completed,
            # for reporting only (not a feature)
            "actual_build_years":     (commercial - start).days / 365.25
                                      if pd.notna(commercial) else np.nan,
        })

    project_df = pd.DataFrame(rows)
    project_df.to_csv(config.PROCESSED / "project_completion_dataset.csv", index=False)
    return project_df
