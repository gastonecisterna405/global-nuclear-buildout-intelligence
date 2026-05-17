from src.models.electricity_supply_scenarios import estimate_generation_twh

def test_generation_formula():
    assert round(estimate_generation_twh(1, .9), 2) == 7.88
