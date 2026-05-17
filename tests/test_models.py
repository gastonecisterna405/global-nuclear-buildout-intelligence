import pandas as pd
import numpy as np


def _make_countries(n: int = 12) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    regions = ["Asia", "Europe", "North America", "Latin America"]
    incomes = ["High income", "Upper middle income", "Lower middle income"]
    return pd.DataFrame({
        "country": [f"Country_{i}" for i in range(n)],
        "region": rng.choice(regions, n),
        "income_group": rng.choice(incomes, n),
        "gdp_current_usd": rng.uniform(1e11, 2e13, n),
        "gdp_per_capita": rng.uniform(3000, 80000, n),
        "population": rng.uniform(1e7, 1.5e9, n),
        "electricity_generation_twh": rng.uniform(50, 5000, n),
        "nuclear_share_percent": rng.uniform(0, 65, n),
        "nuclear_generation_twh": rng.uniform(0, 500, n),
        "operating_capacity_mwe": rng.uniform(0, 100000, n),
        "construction_capacity_mwe": rng.uniform(0, 10000, n),
        "planned_capacity_mwe": rng.uniform(0, 10000, n),
        "proposed_capacity_mwe": rng.uniform(0, 5000, n),
        "average_fleet_age": rng.uniform(0, 50, n),
        "nuclear_experience_years": rng.uniform(0, 70, n),
        "policy_signal_score": rng.uniform(20, 90, n),
        "advanced_reactor_activity_score": rng.uniform(0, 70, n),
    })


def test_capacity_forecaster_output_shape(tmp_path, monkeypatch):
    from src.models import capacity_forecasting_xgboost as mod
    monkeypatch.setattr(mod.config, "PREDICTIONS", tmp_path)
    monkeypatch.setattr(mod.config, "METRICS", tmp_path)
    monkeypatch.setattr(mod.config, "MODELS", tmp_path)
    countries = _make_countries(14)
    out, metrics = mod.train_capacity_forecaster(countries)
    assert len(out) == 14
    assert "forecast_capacity_2035_mwe" in out.columns
    assert "mae" in metrics
    assert metrics["mae"] >= 0


def test_country_clustering_output(tmp_path, monkeypatch):
    from src.models import country_clustering as mod
    monkeypatch.setattr(mod.config, "PREDICTIONS", tmp_path)
    monkeypatch.setattr(mod.config, "METRICS", tmp_path)
    monkeypatch.setattr(mod.config, "MODELS", tmp_path)
    countries = _make_countries(12)
    out, metrics = mod.cluster_countries(countries)
    assert len(out) == 12
    assert "cluster_id" in out.columns
    assert "pca_x" in out.columns
    assert metrics["n_clusters"] >= 2


def test_technology_maturity_score_range():
    from src.features.technology_features import build_technology_taxonomy
    import pandas as pd
    reactors = pd.DataFrame({
        "reactor_type_standardized": ["PWR", "SFR", "SMR-LWR"],
        "status_group": ["Operating", "Operating", "Construction"],
    })
    tax = build_technology_taxonomy(reactors)
    assert tax["maturity_score"].between(0, 100).all(), "maturity_score out of [0,100]"
    assert (tax["maturity_score"] > 0).all()
