from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(
    reactors: pd.DataFrame,
    pipeline: pd.DataFrame,
    scenarios: pd.DataFrame,
    scenario_filter: str,
) -> None:
    cols = st.columns(4)
    cols[0].metric("Operating reactors", int((reactors.status_group == "Operating").sum()))
    cols[1].metric(
        "Operating capacity",
        f"{reactors.loc[reactors.status_group == 'Operating', 'capacity_mwe'].sum() / 1000:,.1f} GWe",
    )
    cols[2].metric("Under construction", int((reactors.status_group == "Construction").sum()))
    cols[3].metric(
        "Construction capacity",
        f"{reactors.loc[reactors.status_group == 'Construction', 'capacity_mwe'].sum() / 1000:,.1f} GWe",
    )

    cols = st.columns(4)
    cols[0].metric(
        "Planned capacity",
        f"{reactors.loc[reactors.status_group == 'Planned', 'capacity_mwe'].sum() / 1000:,.1f} GWe",
    )
    cols[1].metric(
        "Proposed capacity",
        f"{reactors.loc[reactors.status_group == 'Proposed', 'capacity_mwe'].sum() / 1000:,.1f} GWe",
    )
    cols[2].metric("Countries with nuclear records", reactors.country.nunique())

    scenario_twh = 0.0
    if not scenarios.empty:
        mask = (scenarios.year == 2050) & (scenarios.scenario == scenario_filter)
        scenario_twh = scenarios.loc[mask, "estimated_generation_twh"].sum()
    cols[3].metric("2050 scenario TWh", f"{scenario_twh:,.0f}")

    left, right = st.columns([1.2, 1])
    with left:
        cap = (
            reactors.groupby("country", as_index=False)["capacity_mwe"]
            .sum()
            .sort_values("capacity_mwe", ascending=False)
            .head(12)
        )
        st.plotly_chart(
            px.bar(cap, x="country", y="capacity_mwe", title="Capacity by Country",
                   template="plotly_white"),
            use_container_width=True,
        )
    with right:
        st.info(
            "Construction-stage projects and mature LWR technologies drive near-term capacity "
            "confidence. SMR and Gen IV concepts are best read as strategic signals until "
            "deployment history improves."
        )
        if not pipeline.empty:
            st.dataframe(
                pipeline.sort_values("realization_probability", ascending=False).head(5),
                use_container_width=True,
            )
