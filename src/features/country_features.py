from __future__ import annotations
import numpy as np
import pandas as pd
from src import config

def build_country_profiles(reactors: pd.DataFrame, context: pd.DataFrame, pipeline: pd.DataFrame) -> pd.DataFrame:
    grouped = reactors.groupby("country").agg(
        operating_reactor_count=("status_group", lambda s: int((s == "Operating").sum())),
        construction_reactor_count=("status_group", lambda s: int((s == "Construction").sum())),
        planned_reactor_count=("status_group", lambda s: int((s == "Planned").sum())),
        proposed_reactor_count=("status_group", lambda s: int((s == "Proposed").sum())),
        operating_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Operating")].sum())),
        construction_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Construction")].sum())),
        planned_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Planned")].sum())),
        proposed_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Proposed")].sum())),
        average_fleet_age=("age_years", "mean"),
    ).reset_index()
    out = context.merge(grouped, on="country", how="outer")
    out["region"] = out["region"].ffill()
    numeric = [c for c in out.columns if c.endswith("_count") or c.endswith("_mwe") or c in ["average_fleet_age"]]
    out[numeric] = out[numeric].fillna(0)
    flags = pipeline.groupby("country").agg(
        smr_interest_flag=("technology_family", lambda s: bool(s.str.contains("Small Modular|Micro", case=False, na=False).any())),
        geniv_interest_flag=("technology_family", lambda s: bool(s.str.contains("Fast|Molten|Gas|Micro", case=False, na=False).any())),
    ).reset_index()
    out = out.merge(flags, on="country", how="left").fillna({"smr_interest_flag": False, "geniv_interest_flag": False})
    out["advanced_reactor_activity_score"] = (
        out["smr_interest_flag"].astype(int) * 35 + out["geniv_interest_flag"].astype(int) * 35 +
        np.clip(out["planned_capacity_mwe"].fillna(0) / 3000 * 30, 0, 30)
    ).round(1)
    out["policy_signal_score"] = np.clip(35 + out["advanced_reactor_activity_score"] * 0.4 + out["planned_reactor_count"] * 5 + out["construction_reactor_count"] * 8, 0, 100).round(1)
    out["electricity_demand_twh"] = out["electricity_generation_twh"]
    out.to_csv(config.PROCESSED / "country_nuclear_profile.csv", index=False)
    return out
