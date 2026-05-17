from __future__ import annotations
import pandas as pd
from src import config

def build_capacity_scenarios(country: pd.DataFrame, pipeline: pd.DataFrame) -> pd.DataFrame:
    years = [2030, 2040, 2050]
    scenarios = {"Conservative": 0.55, "Base": 0.75, "Accelerated": 0.95}
    rows = []
    for _, c in country.iterrows():
        base_gwe = c.get("operating_capacity_mwe", 0) / 1000
        demand = c.get("electricity_demand_twh", 0)
        p = pipeline[pipeline["country"] == c["country"]]
        for year in years:
            eligible = p[p["expected_operation_year"] <= year]
            for scen, adj in scenarios.items():
                add_gwe = (eligible["capacity_mwe"] * eligible["realization_probability"] * adj).sum() / 1000
                cap = base_gwe + add_gwe
                cf = 0.86
                gen = cap * cf * 8.76
                smr = eligible[eligible["technology_family"].str.contains("Small Modular|Micro", case=False, na=False)]["capacity_mwe"].sum() / 1000 * adj
                geniv = eligible[eligible["technology_family"].str.contains("Fast|Molten|Gas", case=False, na=False)]["capacity_mwe"].sum() / 1000 * adj
                rows.append({
                    "year": year, "country": c["country"], "region": c.get("region"), "scenario": scen,
                    "capacity_gwe": round(cap, 3), "capacity_factor": cf,
                    "estimated_generation_twh": round(gen, 2),
                    "nuclear_share_estimate": round((gen / demand * 100) if demand else 0, 2),
                    "smr_capacity_gwe": round(smr, 3), "geniv_capacity_gwe": round(geniv, 3),
                    "large_reactor_capacity_gwe": round(max(cap - smr - geniv, 0), 3),
                    "source_name": "Scenario engine using processed reactor pipeline and sample/ingested context",
                })
    out = pd.DataFrame(rows)
    out.to_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv", index=False)
    out.to_csv(config.PREDICTIONS / "electricity_supply_scenarios.csv", index=False)
    return out
