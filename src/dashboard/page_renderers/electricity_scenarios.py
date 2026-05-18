from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method


def render(
    scenarios: pd.DataFrame,
    scenario_filter: str,
    capacity_factor: float,
    price: float,
    realization_adjustment: float,
) -> None:
    s = scenarios[scenarios.scenario == scenario_filter].copy()
    s["estimated_generation_twh_adjusted"] = (
        s.capacity_gwe * capacity_factor * 8.76 * realization_adjustment
    )
    s["estimated_market_value_usd"] = s.estimated_generation_twh_adjusted * 1_000_000 * price

    left, right = st.columns(2)
    left.metric(
        "Estimated scenario generation",
        f"{s.estimated_generation_twh_adjusted.sum():,.0f} TWh/year",
    )
    right.metric(
        "Estimated market value proxy",
        f"${s.estimated_market_value_usd.sum() / 1e9:,.1f}B",
    )

    annual = s.groupby("year", as_index=False)["estimated_generation_twh_adjusted"].sum()
    st.plotly_chart(
        px.line(
            annual, x="year", y="estimated_generation_twh_adjusted",
            title="Scenario Generation Sensitivity", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(s, use_container_width=True)
    _method(
        data="nuclear_capacity_scenarios.csv (Conservative/Base/Accelerated scenarios × 3 years × 34 countries)",
        features="capacity_gwe · realization_probability weighted by scenario adjustment factor · capacity_factor (user-controlled) · price_per_mwh (user-controlled)",
        model="Scenario engine: TWh/yr = capacity_GW × capacity_factor × 8.76 × realization_adjustment. No ML model — deterministic scenario arithmetic.",
        notes="Not a market forecast. Capacity factor, realization adjustment, and price are user-configurable sensitivity parameters."
    )
