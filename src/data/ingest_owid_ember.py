from __future__ import annotations

import io
import logging

import pandas as pd
import requests

from src import config

logger = logging.getLogger(__name__)

OWID_URL = (
    "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
)

KEEP_COLS = [
    "country", "year",
    "nuclear_electricity",      # TWh generated
    "nuclear_share_elec",       # % of electricity from nuclear
    "nuclear_elec_per_capita",  # kWh per person
    "electricity_demand",       # TWh total
    "gdp",                      # USD (constant)
    "population",
    "primary_energy_consumption",
    "coal_electricity",
    "renewables_electricity",
    "low_carbon_electricity",
    "energy_per_capita",
]

# Aggregate regions / income groups excluded — we want country rows only
EXCLUDE_AGGREGATES = {
    "World", "Asia", "Europe", "Africa", "North America", "South America",
    "Oceania", "European Union (27)", "OECD (EI)", "Non-OECD (EI)",
    "Asia Pacific (EI)", "CIS (EI)", "North America (EI)",
    "South and Central America (EI)", "Middle East (EI)", "Africa (EI)",
    "Europe (EI)", "High-income countries", "Upper-middle-income countries",
    "Lower-middle-income countries", "Low-income countries",
}


def ingest_owid(timeout: int = 30) -> pd.DataFrame:
    out_dir = config.RAW / "our_world_in_data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "owid_energy_data.csv"

    try:
        r = requests.get(OWID_URL, timeout=timeout)
        r.raise_for_status()
        raw = pd.read_csv(io.BytesIO(r.content))
        raw.to_csv(out_path, index=False)
        logger.info("OWID downloaded: %d rows", len(raw))
    except Exception as exc:
        logger.warning("OWID download failed: %s — trying cached file.", exc)
        if out_path.exists():
            raw = pd.read_csv(out_path)
        else:
            (out_dir / "DOWNLOAD_FAILED.txt").write_text(str(exc), encoding="utf-8")
            return pd.DataFrame()

    available = [c for c in KEEP_COLS if c in raw.columns]
    df = (
        raw[available]
        .copy()
        .query("country not in @EXCLUDE_AGGREGATES")
        .query("year >= 1965")
        .sort_values(["country", "year"])
        .reset_index(drop=True)
    )

    # Save clean version for the pipeline to use
    clean_path = config.RAW / "our_world_in_data" / "owid_nuclear_clean.csv"
    df.to_csv(clean_path, index=False)
    logger.info("OWID clean: %d rows, %d countries, %d-%d",
                len(df), df.country.nunique(), df.year.min(), df.year.max())
    return df
