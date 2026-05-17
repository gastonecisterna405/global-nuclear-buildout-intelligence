import pandas as pd
import numpy as np
from src.models.electricity_supply_scenarios import estimate_generation_twh


def test_generation_formula():
    assert round(estimate_generation_twh(1, 0.9), 2) == 7.88


def test_generation_zero_capacity():
    assert estimate_generation_twh(0, 0.9) == 0.0


def test_generation_scales_with_capacity():
    assert estimate_generation_twh(2, 0.86) > estimate_generation_twh(1, 0.86)


def test_scenario_builder_output_shape(tmp_path, monkeypatch):
    from src.features import scenario_features as mod
    monkeypatch.setattr(mod.config, "PROCESSED", tmp_path)
    monkeypatch.setattr(mod.config, "PREDICTIONS", tmp_path)
    from src.features.scenario_features import build_capacity_scenarios

    countries = pd.DataFrame([{
        "country": "X", "region": "Asia",
        "operating_capacity_mwe": 5000.0,
        "electricity_demand_twh": 300.0,
    }])
    pipeline = pd.DataFrame([{
        "country": "X", "technology_family": "Light Water Reactor",
        "capacity_mwe": 1000.0, "realization_probability": 0.8,
        "expected_operation_year": 2030,
    }])
    out = build_capacity_scenarios(countries, pipeline)
    # 3 scenarios × 3 years × 1 country = 9 rows
    assert len(out) == 9
    assert set(out["scenario"].unique()) == {"Conservative", "Base", "Accelerated"}
    assert out["estimated_generation_twh"].gt(0).all()


def test_scenario_conservative_less_than_accelerated(tmp_path, monkeypatch):
    from src.features import scenario_features as mod
    monkeypatch.setattr(mod.config, "PROCESSED", tmp_path)
    monkeypatch.setattr(mod.config, "PREDICTIONS", tmp_path)
    from src.features.scenario_features import build_capacity_scenarios

    countries = pd.DataFrame([{
        "country": "X", "region": "Asia",
        "operating_capacity_mwe": 5000.0,
        "electricity_demand_twh": 300.0,
    }])
    pipeline = pd.DataFrame([{
        "country": "X", "technology_family": "Light Water Reactor",
        "capacity_mwe": 2000.0, "realization_probability": 0.8,
        "expected_operation_year": 2030,
    }])
    out = build_capacity_scenarios(countries, pipeline)
    y2030 = out[out.year == 2030]
    cons = y2030[y2030.scenario == "Conservative"]["estimated_generation_twh"].iloc[0]
    accel = y2030[y2030.scenario == "Accelerated"]["estimated_generation_twh"].iloc[0]
    assert cons < accel
