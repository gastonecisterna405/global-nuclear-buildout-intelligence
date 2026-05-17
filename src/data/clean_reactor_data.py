from __future__ import annotations

import re
import numpy as np
import pandas as pd
from src import config
from src.utils.constants import REGIONS, STATUS_GROUPS, TECHNOLOGY_FAMILY

def _num(x):
    if pd.isna(x):
        return np.nan
    return float(str(x).replace(",", "").strip())

def standardize_status(status: str) -> str:
    s = re.sub(r"[-_]+", " ", str(status).strip().lower())
    return STATUS_GROUPS.get(s, STATUS_GROUPS.get(s.replace("  ", " "), str(status).strip().title()))

def standardize_reactor_type(raw: str, design: str | None = None) -> str:
    text = f"{raw} {design or ''}".upper()
    if "AP1000" in text: return "AP1000"
    if "EPR" in text: return "EPR"
    if "VVER" in text: return "VVER"
    if "APR1400" in text: return "PWR"
    if "BWRX" in text or "SMR" in text or "CAREM" in text: return "SMR-LWR"
    if "PHWR" in text or "CANDU" in text: return "PHWR"
    if "BWR" in text: return "BWR"
    if "SFR" in text or "NATRIUM" in text: return "SFR"
    if "FBR" in text or "BN-" in text: return "FBR"
    if "MSR" in text or "MOLTEN" in text: return "MSR"
    if "HTGR" in text or "HTR" in text: return "HTGR"
    return str(raw).strip().upper()

def clean_reactors() -> pd.DataFrame:
    path = config.RAW / "sample" / "dirty_reactors_raw.csv"
    df = pd.read_csv(path)
    df["reactor_name"] = df["reactor_name"].astype(str).str.strip()
    df["reactor_id"] = (
        df["country"].astype(str).str.upper().str[:3] + "-" +
        df["plant_name"].astype(str).str.upper().str.replace(r"[^A-Z0-9]+", "-", regex=True) + "-" +
        df["unit_name"].astype(str).str.upper().str.replace(r"[^A-Z0-9]+", "-", regex=True)
    )
    df["net_capacity_mwe"] = df["net_capacity_mwe"].map(_num)
    df["gross_capacity_mwe"] = df["gross_capacity_mwe"].map(_num)
    df["capacity_mwe"] = df["net_capacity_mwe"].fillna(df["gross_capacity_mwe"])
    df["status_group"] = df["status"].map(standardize_status)
    df["status"] = df["status"].astype(str).str.strip().str.replace("-", " ").str.title()
    df["reactor_type_standardized"] = [standardize_reactor_type(r, d) for r, d in zip(df["reactor_type"], df["design_name"])]
    df["technology_family"] = df["reactor_type_standardized"].map(TECHNOLOGY_FAMILY).fillna("Other/Unclassified")
    df["generation_category"] = np.select(
        [
            df["reactor_type_standardized"].isin(["AP1000", "EPR", "VVER", "PWR"]),
            df["reactor_type_standardized"].isin(["SMR-LWR", "SFR", "MSR", "HTGR", "FBR"]),
        ],
        ["Gen III/III+ or modern LWR", "Advanced/Gen IV candidate"],
        default="Gen II/legacy or unspecified",
    )
    df["size_category"] = pd.cut(df["capacity_mwe"], bins=[0, 50, 300, 700, 2000], labels=["Micro/small", "SMR", "Mid-size", "Large"], include_lowest=True).astype(str)
    for col in ["construction_start_date", "grid_connection_date", "commercial_operation_date", "shutdown_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    df["construction_start_year"] = df["construction_start_date"].dt.year
    df["expected_start_year"] = np.where(df["status_group"].isin(["Construction", "Planned", "Proposed"]), np.nan, df["commercial_operation_date"].dt.year)
    df["age_years"] = np.where(df["commercial_operation_date"].notna(), config.CURRENT_YEAR - df["commercial_operation_date"].dt.year, np.nan)
    df["region"] = df["country"].map(REGIONS).fillna("Other")
    df["source_confidence"] = np.where(df["source_name"].str.contains("Sample", case=False, na=False), 0.55, 0.8)
    df["source_last_updated"] = "2026-05-17"
    df = df.sort_values(["source_confidence", "reactor_id"], ascending=[False, True]).drop_duplicates("reactor_id", keep="first")
    cols = [
        "reactor_id","reactor_name","unit_name","plant_name","country","region","latitude","longitude",
        "status","status_group","reactor_type","reactor_type_standardized","technology_family",
        "generation_category","size_category","capacity_mwe","gross_capacity_mwe","net_capacity_mwe",
        "construction_start_date","grid_connection_date","commercial_operation_date","shutdown_date",
        "expected_start_year","age_years","owner","operator","vendor","source_name","source_confidence",
        "source_last_updated"
    ]
    out = df[cols]
    out.to_csv(config.PROCESSED / "reactors_master.csv", index=False)
    return out
