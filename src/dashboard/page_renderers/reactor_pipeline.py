from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method

STATUS_COLORS = {
    "Construction": "#f59e0b", "Planned": "#10b981",
    "Proposed": "#8b5cf6", "Paused": "#94a3b8",
}

DISPLAY_COLS = {
    "reactor_name": "Project", "country": "Country",
    "technology_family": "Technology", "capacity_mwe": "MWe",
    "status_group": "Status", "expected_operation_year": "Expected year",
    "project_maturity_score": "Maturity", "delay_risk_score": "Delay risk",
    "realization_probability": "Prob.",
}


def render(pipeline: pd.DataFrame) -> None:
    if pipeline.empty:
        st.warning("No pipeline data. Run `python run_pipeline.py`.")
        return

    # KPI strip
    cols = st.columns(4)
    cols[0].metric("Pipeline projects", len(pipeline))
    cols[1].metric("Total pipeline capacity",
                   f"{pipeline.capacity_mwe.sum() / 1000:.1f} GWe")
    cols[2].metric("Under construction",
                   int((pipeline.status_group == "Construction").sum()))
    cols[3].metric("Avg. maturity score",
                   f"{pipeline.project_maturity_score.mean():.0f} / 100")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.markdown("**Expected capacity additions by year (GWe)**")
        timeline = (
            pipeline.groupby("expected_operation_year", as_index=False)["capacity_mwe"]
            .sum()
            .assign(capacity_gwe=lambda df: df.capacity_mwe / 1000)
            .rename(columns={"expected_operation_year": "Year", "capacity_gwe": "GWe"})
        )
        fig = px.bar(timeline, x="Year", y="GWe",
                     template="plotly_white",
                     color_discrete_sequence=["#2563eb"])
        fig.update_layout(margin=dict(t=10), xaxis=dict(type="category"))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("**Pipeline funnel by technology and status**")
        funnel = (
            pipeline.groupby(["technology_family", "status_group"], as_index=False)["capacity_mwe"]
            .sum()
            .rename(columns={"technology_family": "Technology",
                             "status_group": "Status", "capacity_mwe": "MWe"})
        )
        fig2 = px.bar(funnel, x="Technology", y="MWe", color="Status",
                      color_discrete_map=STATUS_COLORS,
                      template="plotly_white")
        fig2.update_layout(margin=dict(t=10), xaxis_title="",
                           xaxis=dict(tickangle=-25))
        st.plotly_chart(fig2, use_container_width=True)

    # Risk vs maturity scatter
    st.markdown("**Maturity vs delay risk — all projects**")
    fig3 = px.scatter(
        pipeline,
        x="project_maturity_score", y="delay_risk_score",
        size="capacity_mwe", color="status_group",
        hover_name="reactor_name",
        hover_data={"country": True, "technology_family": True,
                    "capacity_mwe": True, "realization_probability": True},
        color_discrete_map=STATUS_COLORS,
        labels={"project_maturity_score": "Maturity score",
                "delay_risk_score": "Delay risk score",
                "status_group": "Status"},
        template="plotly_white",
        size_max=40,
    )
    fig3.update_layout(margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

    # Table
    st.markdown("**All pipeline projects**")
    show_cols = [c for c in DISPLAY_COLS if c in pipeline.columns]
    st.dataframe(
        pipeline[show_cols]
        .rename(columns=DISPLAY_COLS)
        .sort_values("Maturity", ascending=False),
        use_container_width=True, hide_index=True,
    )
    _method(
        data="reactor_pipeline.csv — UC/Planned/Proposed projects with scoring",
        features="project_maturity_score (45% status stage + 25% tech maturity + 20% country experience + 10% GDP) · delay_risk_score (100 − maturity + large-unit penalty) · realization_probability (maturity/100)",
        notes="No ML model — transparent heuristic scoring. Labels are auditable formulas, not statistical predictions."
    )
