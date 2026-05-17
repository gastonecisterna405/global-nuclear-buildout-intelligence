from __future__ import annotations

import numpy as np
import pandas as pd
from src import config


def _capacity_by_status(reactors: pd.DataFrame, status: str) -> pd.Series:
    return (
        reactors[reactors["status_group"] == status]
        .groupby("country")["capacity_mwe"]
        .sum()
    )


def build_country_profiles(
    reactors: pd.DataFrame,
    context: pd.DataFrame,
    pipeline: pd.DataFrame,
) -> pd.DataFrame:
    counts = reactors.groupby("country")["status_group"].value_counts().unstack(fill_value=0)
    for col in ["Operating", "Construction", "Planned", "Proposed"]:
        if col not in counts.columns:
            counts[col] = 0
    counts = counts.rename(columns={
        "Operating": "operating_reactor_count",
        "Construction": "construction_reactor_count",
        "Planned": "planned_reactor_count",
        "Proposed": "proposed_reactor_count",
    })[["operating_reactor_count", "construction_reactor_count", "planned_reactor_count", "proposed_reactor_count"]]

    capacities = pd.DataFrame({
        "operating_capacity_mwe": _capacity_by_status(reactors, "Operating"),
        "construction_capacity_mwe": _capacity_by_status(reactors, "Construction"),
        "planned_capacity_mwe": _capacity_by_status(reactors, "Planned"),
        "proposed_capacity_mwe": _capacity_by_status(reactors, "Proposed"),
        "average_fleet_age": reactors.groupby("country")["age_years"].mean(),
    })

    grouped = counts.join(capacities, how="outer").reset_index()
    out = context.merge(grouped, on="country", how="outer")
    out["region"] = out["region"].ffill()

    numeric_cols = [c for c in out.columns if c.endswith("_count") or c.endswith("_mwe") or c == "average_fleet_age"]
    out[numeric_cols] = out[numeric_cols].fillna(0)

    flags = pipeline.groupby("country").agg(
        smr_interest_flag=("technology_family", lambda s: bool(s.str.contains("Small Modular|Micro", case=False, na=False).any())),
        geniv_interest_flag=("technology_family", lambda s: bool(s.str.contains("Fast|Molten|Gas|Micro", case=False, na=False).any())),
    ).reset_index()
    out = out.merge(flags, on="country", how="left").fillna({"smr_interest_flag": False, "geniv_interest_flag": False})

    out["advanced_reactor_activity_score"] = (
        out["smr_interest_flag"].astype(int) * 35
        + out["geniv_interest_flag"].astype(int) * 35
        + np.clip(out["planned_capacity_mwe"].fillna(0) / 3000 * 30, 0, 30)
    ).round(1)

    out["policy_signal_score"] = np.clip(
        35
        + out["advanced_reactor_activity_score"] * 0.4
        + out["planned_reactor_count"] * 5
        + out["construction_reactor_count"] * 8,
        0, 100,
    ).round(1)

    out["electricity_demand_twh"] = out["electricity_generation_twh"]
    out.to_csv(config.PROCESSED / "country_nuclear_profile.csv", index=False)
    return out
