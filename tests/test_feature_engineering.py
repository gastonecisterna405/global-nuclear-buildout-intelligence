import pandas as pd
import numpy as np
import pytest
from src.features.reactor_features import add_reactor_feature_flags


def _base_reactor(**kwargs):
    row = {
        "reactor_id": "A", "reactor_name": "R1", "country": "X", "region": "Asia",
        "status": "Operating", "status_group": "Operating", "reactor_type_standardized": "PWR",
        "technology_family": "Light Water Reactor", "capacity_mwe": 1000.0,
        "construction_start_date": pd.NaT, "construction_start_year": np.nan,
        "commercial_operation_date": pd.Timestamp("2000-01-01"),
        "age_years": 26.0, "latitude": 30.0, "longitude": 100.0,
        "source_name": "Sample",
    }
    row.update(kwargs)
    return pd.DataFrame([row])


def test_smr_flag_set():
    df = pd.DataFrame([{"reactor_type_standardized": "SMR-LWR", "technology_family": "Small Modular Reactor"}])
    out = add_reactor_feature_flags(df)
    assert out.loc[0, "smr_flag"]
    assert not out.loc[0, "molten_salt_flag"]


def test_msr_flags_set():
    df = pd.DataFrame([{"reactor_type_standardized": "MSR", "technology_family": "Molten Salt Reactor"}])
    out = add_reactor_feature_flags(df)
    assert out.loc[0, "molten_salt_flag"]
    assert out.loc[0, "geniv_flag"]


def test_pwr_no_advanced_flags():
    df = pd.DataFrame([{"reactor_type_standardized": "PWR", "technology_family": "Light Water Reactor"}])
    out = add_reactor_feature_flags(df)
    assert not out.loc[0, "smr_flag"]
    assert not out.loc[0, "geniv_flag"]
    assert not out.loc[0, "molten_salt_flag"]


def test_country_profiles_capacity_sum(tmp_path, monkeypatch):
    from src.features import country_features as mod
    monkeypatch.setattr(mod.config, "PROCESSED", tmp_path)

    reactors = pd.DataFrame([
        {"reactor_id": "A", "country": "X", "region": "Asia", "status_group": "Operating",
         "capacity_mwe": 1000.0, "age_years": 20.0,
         "reactor_type_standardized": "PWR", "technology_family": "Light Water Reactor"},
        {"reactor_id": "B", "country": "X", "region": "Asia", "status_group": "Construction",
         "capacity_mwe": 1200.0, "age_years": np.nan,
         "reactor_type_standardized": "AP1000", "technology_family": "Light Water Reactor"},
    ])
    context = pd.DataFrame([{
        "country": "X", "region": "Asia", "income_group": "High income",
        "gdp_current_usd": 1e12, "gdp_per_capita": 50000, "population": 1e7,
        "electricity_generation_twh": 400, "nuclear_share_percent": 20.0,
        "nuclear_generation_twh": 80.0, "nuclear_experience_years": 40,
        "historical_completed_reactors": 5,
    }])
    pipeline = pd.DataFrame(columns=["country", "technology_family", "capacity_mwe"])
    out = mod.build_country_profiles(reactors, context, pipeline)
    row = out[out.country == "X"].iloc[0]
    assert row["operating_capacity_mwe"] == 1000.0
    assert row["construction_capacity_mwe"] == 1200.0
    assert row["planned_capacity_mwe"] == 0.0


def test_pipeline_maturity_score_range(tmp_path, monkeypatch):
    from src.features import technology_features as tmod
    from src.features import pipeline_features as pmod
    monkeypatch.setattr(tmod.config, "PROCESSED", tmp_path)
    monkeypatch.setattr(pmod.config, "PROCESSED", tmp_path)

    reactors = _base_reactor(status_group="Construction", construction_start_year=2020.0)
    tax = tmod.build_technology_taxonomy(reactors)
    context = pd.DataFrame([{
        "country": "X", "region": "Asia", "income_group": "High income",
        "gdp_current_usd": 1e12, "gdp_per_capita": 50000, "population": 1e7,
        "electricity_generation_twh": 400, "nuclear_share_percent": 20,
        "nuclear_generation_twh": 80, "nuclear_experience_years": 40,
        "historical_completed_reactors": 5,
    }])
    pipeline = pmod.build_reactor_pipeline(reactors, tax, context)
    score = pipeline["project_maturity_score"].iloc[0]
    assert 0 <= score <= 100, f"maturity_score out of range: {score}"
