from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import config

STATUS_COLORS = {
    "Operating":     "#2563eb",
    "Construction":  "#f59e0b",
    "Planned":       "#10b981",
    "Proposed":      "#8b5cf6",
    "Paused":        "#94a3b8",
    "Shutdown":      "#ef4444",
}


def render(
    reactors: pd.DataFrame,
    pipeline: pd.DataFrame,
    scenarios: pd.DataFrame,
    scenario_filter: str,
) -> None:
    st.subheader(f"Global Fleet — as of {config.CURRENT_YEAR}")

    # ── KPI row 1: operating fleet ────────────────────────────────────────────
    op = reactors[reactors.status_group == "Operating"]
    uc = reactors[reactors.status_group == "Construction"]
    cols = st.columns(4)
    cols[0].metric("Operating units",     int(len(op)))
    cols[1].metric("Operating capacity",  f"{op.capacity_mwe.sum() / 1000:,.1f} GWe")
    cols[2].metric("Under construction",  int(len(uc)))
    cols[3].metric("Construction capacity", f"{uc.capacity_mwe.sum() / 1000:,.1f} GWe")

    # ── KPI row 2: pipeline + context ─────────────────────────────────────────
    pl = reactors[reactors.status_group == "Planned"]
    pr = reactors[reactors.status_group == "Proposed"]
    scenario_twh = 0.0
    if not scenarios.empty:
        mask = (scenarios.year == 2050) & (scenarios.scenario == scenario_filter)
        scenario_twh = scenarios.loc[mask, "estimated_generation_twh"].sum()

    cols = st.columns(4)
    cols[0].metric("Planned capacity",   f"{pl.capacity_mwe.sum() / 1000:,.1f} GWe")
    cols[1].metric("Proposed capacity",  f"{pr.capacity_mwe.sum() / 1000:,.1f} GWe")
    cols[2].metric("Countries tracked",  reactors.country.nunique())
    cols[3].metric(f"2050 {scenario_filter} scenario", f"{scenario_twh:,.0f} TWh/yr")

    st.divider()

    # ── Charts ────────────────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown("**Operating capacity by country (GWe)**")
        cap = (
            op.groupby("country")["capacity_mwe"]
            .sum()
            .div(1000)
            .sort_values(ascending=False)
            .head(12)
            .reset_index()
            .rename(columns={"capacity_mwe": "Operating capacity (GWe)"})
        )
        fig = px.bar(
            cap, x="country", y="Operating capacity (GWe)",
            template="plotly_white",
            color_discrete_sequence=["#2563eb"],
        )
        fig.update_layout(
            margin=dict(t=10, b=0),
            xaxis_title="",
            yaxis_title="GWe",
            font=dict(size=12),
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("**Capacity by status (all tracked units)**")
        by_status = (
            reactors.groupby("status_group")["capacity_mwe"]
            .sum()
            .div(1000)
            .reset_index()
            .rename(columns={"capacity_mwe": "GWe", "status_group": "Status"})
        )
        by_status["color"] = by_status["Status"].map(STATUS_COLORS)
        fig2 = px.bar(
            by_status.sort_values("GWe", ascending=True),
            x="GWe", y="Status", orientation="h",
            template="plotly_white",
            color="Status",
            color_discrete_map=STATUS_COLORS,
        )
        fig2.update_layout(
            margin=dict(t=10, b=0),
            showlegend=False,
            font=dict(size=12),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Top pipeline projects ─────────────────────────────────────────────────
    if not pipeline.empty:
        st.markdown("**Highest-confidence pipeline projects**")
        top = (
            pipeline.sort_values("realization_probability", ascending=False)
            .head(6)[["reactor_name", "country", "technology_family",
                       "capacity_mwe", "status_group",
                       "project_maturity_score", "realization_probability"]]
            .rename(columns={
                "reactor_name": "Project",
                "country": "Country",
                "technology_family": "Technology",
                "capacity_mwe": "MWe",
                "status_group": "Status",
                "project_maturity_score": "Maturity",
                "realization_probability": "Prob.",
            })
        )
        st.dataframe(top, use_container_width=True, hide_index=True)
