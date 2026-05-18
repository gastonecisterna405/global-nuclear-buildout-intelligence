from __future__ import annotations

import io
import logging

import pandas as pd
import requests

from src import config

logger = logging.getLogger(__name__)

# GEM publishes updated snapshots; try several known URL patterns in order.
_GEM_URLS = [
    "https://globalenergymonitor.org/wp-content/uploads/2025/04/GlobalNuclearPowerTracker-April2025.xlsx",
    "https://globalenergymonitor.org/wp-content/uploads/2025/01/GlobalNuclearPowerTracker-January2025.xlsx",
    "https://globalenergymonitor.org/wp-content/uploads/2024/11/GlobalNuclearPowerTracker-November2024.xlsx",
    "https://globalenergymonitor.org/wp-content/uploads/2024/09/GlobalNuclearPowerTracker-September2024.xlsx",
    "https://globalenergymonitor.org/wp-content/uploads/2024/05/GlobalNuclearPowerTracker-May2024.xlsx",
    "https://globalenergymonitor.org/wp-content/uploads/2024/01/GlobalNuclearPowerTracker-January2024.xlsx",
]

# Map GEM column names → our schema (approximate; GEM sheet headers vary slightly)
_COL_MAP = {
    "Plant": "plant_name",
    "Unit": "unit_name",
    "Country": "country",
    "Status": "status",
    "Capacity (MW)": "net_capacity_mwe",
    "Reactor Type": "reactor_type",
    "Construction Start": "construction_start_date",
    "Grid Connection": "grid_connection_date",
    "Commercial Operation": "commercial_operation_date",
    "Retire Date": "shutdown_date",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Owner": "owner",
    "Operator": "operator",
    "Fuel": "fuel_type",
    "Wiki URL": "source_url",
}


def _try_download(timeout: int = 30) -> bytes | None:
    for url in _GEM_URLS:
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200 and len(r.content) > 50_000:
                logger.info("Downloaded GEM data from %s (%d bytes)", url, len(r.content))
                return r.content
        except Exception as exc:
            logger.debug("GEM URL %s failed: %s", url, exc)
    return None


def _parse_gem_excel(raw: bytes) -> pd.DataFrame:
    xls = pd.ExcelFile(io.BytesIO(raw))
    # GEM typically has a sheet called "Nuclear Power Tracker" or similar
    target_sheet = None
    for sheet in xls.sheet_names:
        if "nuclear" in sheet.lower() or "tracker" in sheet.lower() or "data" in sheet.lower():
            target_sheet = sheet
            break
    target_sheet = target_sheet or xls.sheet_names[0]

    df = pd.read_excel(xls, sheet_name=target_sheet, dtype=str)
    df.columns = df.columns.str.strip()

    # Rename columns we recognise
    rename = {k: v for k, v in _COL_MAP.items() if k in df.columns}
    df = df.rename(columns=rename)

    # Build reactor_name from plant + unit
    if "plant_name" in df.columns and "unit_name" in df.columns:
        df["reactor_name"] = (
            df["plant_name"].fillna("").str.strip()
            + "-"
            + df["unit_name"].fillna("").str.strip()
        ).str.strip("-")
    elif "plant_name" in df.columns:
        df["reactor_name"] = df["plant_name"].str.strip()

    # Ensure required columns exist
    for col in ["reactor_name", "plant_name", "unit_name", "country", "status",
                "reactor_type", "net_capacity_mwe", "latitude", "longitude"]:
        if col not in df.columns:
            df[col] = ""

    df["source_name"] = "Global Energy Monitor Nuclear Power Tracker"
    return df


def ingest_gem(timeout: int = 30) -> pd.DataFrame:
    out_dir = config.RAW / "gem"
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = _try_download(timeout=timeout)
    if raw is None:
        marker = out_dir / "DOWNLOAD_FAILED.txt"
        marker.write_text(
            "GEM Nuclear Power Tracker download failed. "
            "Pipeline will use comprehensive sample data.\n",
            encoding="utf-8",
        )
        return pd.DataFrame()

    try:
        df = _parse_gem_excel(raw)
        out_path = out_dir / "gem_nuclear_power_tracker.xlsx"
        out_path.write_bytes(raw)
        csv_path = out_dir / "gem_nuclear_power_tracker.csv"
        df.to_csv(csv_path, index=False)
        logger.info("GEM data: %d reactor records across %d countries", len(df), df["country"].nunique())
        return df
    except Exception as exc:
        logger.warning("GEM parse error: %s", exc)
        (out_dir / "PARSE_FAILED.txt").write_text(str(exc), encoding="utf-8")
        return pd.DataFrame()
