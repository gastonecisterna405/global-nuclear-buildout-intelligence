from __future__ import annotations
import numpy as np
import pandas as pd
from src import config

def build_reactor_pipeline(reactors: pd.DataFrame, taxonomy: pd.DataFrame, countries: pd.DataFrame) -> pd.DataFrame:
    df = reactors[reactors["status_group"].isin(["Construction", "Planned", "Proposed", "Paused"])].copy()
    tax = taxonomy[["reactor_type","maturity_score"]].rename(columns={"reactor_type":"reactor_type_standardized"})
    df = df.merge(tax, on="reactor_type_standardized", how="left")
    df = df.merge(countries[["country","gdp_current_usd","nuclear_experience_years","historical_completed_reactors"]], on="country", how="left")
    if "construction_start_year" not in df.columns:
        df["construction_start_year"] = pd.to_datetime(df["construction_start_date"], errors="coerce").dt.year
    stage_score = df["status_group"].map({"Construction": 85, "Planned": 55, "Proposed": 30, "Paused": 20}).fillna(35)
    experience = np.clip(df["nuclear_experience_years"].fillna(0) / 70 * 100, 0, 100)
    tech = df["maturity_score"].fillna(35)
    gdp = np.clip(np.log10(df["gdp_current_usd"].fillna(1)) / 14 * 100, 0, 100)
    df["project_maturity_score"] = (0.45 * stage_score + 0.25 * tech + 0.20 * experience + 0.10 * gdp).round(1)
    df["delay_risk_score"] = (100 - df["project_maturity_score"] + np.where(df["capacity_mwe"] > 1200, 7, 0) + np.where(df["status_group"].eq("Proposed"), 8, 0)).clip(0, 100).round(1)
    df["realization_probability"] = (df["project_maturity_score"] / 100).clip(0.05, 0.95).round(2)
    df["expected_operation_year"] = np.select(
        [df["status_group"].eq("Construction"), df["status_group"].eq("Planned"), df["status_group"].eq("Proposed")],
        [2030, 2035, 2042],
        default=2045,
    )
    df["delay_years_if_known"] = np.where(df["construction_start_year"].notna(), np.maximum(0, config.CURRENT_YEAR - df["construction_start_year"] - 7), np.nan)
    df["project_stage"] = df["status_group"]
    df["project_id"] = "PIPE-" + df["reactor_id"].astype(str)
    cols = ["project_id","reactor_name","country","status","status_group","technology_family","reactor_type_standardized","capacity_mwe","construction_start_year","expected_operation_year","delay_years_if_known","project_stage","project_maturity_score","delay_risk_score","realization_probability","source_name"]
    out = df[cols].rename(columns={"reactor_type_standardized":"reactor_type"})
    out.to_csv(config.PROCESSED / "reactor_pipeline.csv", index=False)
    return out
