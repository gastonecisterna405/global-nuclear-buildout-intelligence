from __future__ import annotations

import json
import pandas as pd
from src import config

def run_data_quality_checks(reactors: pd.DataFrame, countries: pd.DataFrame) -> dict:
    missing = reactors.isna().mean().sort_values(ascending=False).round(3).to_dict()
    coverage = reactors.groupby("country").size().sort_values(ascending=False).to_dict()
    duplicates = int(reactors.duplicated("reactor_id").sum())
    confidence = reactors.groupby("source_name")["source_confidence"].mean().round(2).to_dict()
    quality = {
        "reactor_rows": int(len(reactors)),
        "country_rows": int(len(countries)),
        "duplicate_reactor_ids": duplicates,
        "missing_fraction_by_field": missing,
        "source_confidence": confidence,
        "source_coverage_by_country": coverage,
        "sample_data_warning": "Raw fallback data is labeled sample-only and is intended to be replaced or augmented by manual/official source exports.",
    }
    (config.METRICS / "data_quality_metrics.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    pd.DataFrame({"field": list(missing), "missing_fraction": list(missing.values())}).to_csv(config.ANALYTICS / "missingness_by_field.csv", index=False)
    return quality
