from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

DISPLAY_COLS = {
    "reactor_name": "Reactor", "status_group": "Status",
    "reactor_type_standardized": "Type", "capacity_mwe": "MWe",
    "commercial_operation_date": "Commercial operation",
}

PIPELINE_COLS = {
    "reactor_name": "Project", "status_group": "Status",
    "technology_family": "Technology", "capacity_mwe": "MWe",
    "project_maturity_score": "Maturity", "delay_risk_score": "Delay risk",
    "realization_probability": "Prob.",
}

STATUS_COLORS = {
    "Operating": "#2563eb", "Construction": "#f59e0b",
    "Planned": "#10b981", "Proposed": "#8b5cf6",
    "Paused": "#94a3b8", "Shutdown": "#ef4444",
}


def render(
    reactors: pd.DataFrame,
    countries: pd.DataFrame,
    pipeline: pd.DataFrame,
) -> None:
    all_countries = sorted(countries.country.dropna().unique())
    if not all_countries:
        st.warning("No country data available.")
        return

    selected = st.selectbox("Select country", all_countries)
    cr = reactors[reactors.country == selected]
    cp = pipeline[pipeline.country == selected] if not pipeline.empty else pd.DataFrame()
    cx = countries[countries.country == selected]

    st.subheader(selected)

    # KPI strip
    if not cx.empty:
        row = cx.iloc[0]
        cols = st.columns(4)
        cols[0].metric("Operating capacity",
                       f"{row.get('operating_capacity_mwe', 0) / 1000:.1f} GWe")
        cols[1].metric("Nuclear share",
                       f"{row.get('nuclear_share_percent', 0):.1f}%")
        cols[2].metric("Nuclear experience",
                       f"{int(row.get('nuclear_experience_years', 0))} yr")
        cols[3].metric("Pipeline projects",
                       int(len(cp)))

    st.divider()

    # Fleet + tech mix charts
    left, right = st.columns(2)
    with left:
        st.markdown("**Fleet by status (MWe)**")
        if not cr.empty:
            data = (
                cr.groupby("status_group", as_index=False)["capacity_mwe"]
                .sum()
                .rename(columns={"status_group": "Status", "capacity_mwe": "MWe"})
            )
            fig = px.bar(data, x="Status", y="MWe",
                         color="Status", color_discrete_map=STATUS_COLORS,
                         template="plotly_white")
            fig.update_layout(showlegend=False, margin=dict(t=10), xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No reactor records for this country.")

    with right:
        st.markdown("**Technology mix (MWe)**")
        if not cr.empty:
            data = (
                cr.groupby("technology_family", as_index=False)["capacity_mwe"]
                .sum()
                .rename(columns={"technology_family": "Technology", "capacity_mwe": "MWe"})
                .sort_values("MWe", ascending=False)
            )
            fig = px.bar(data, x="Technology", y="MWe",
                         template="plotly_white",
                         color_discrete_sequence=["#10b981"])
            fig.update_layout(margin=dict(t=10), xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No reactor records for this country.")

    # Reactor table
    if not cr.empty:
        st.markdown("**All reactor records**")
        show_cols = [c for c in DISPLAY_COLS if c in cr.columns]
        st.dataframe(
            cr[show_cols].rename(columns=DISPLAY_COLS),
            use_container_width=True, hide_index=True,
        )

    # Pipeline table
    if not cp.empty:
        st.markdown("**Pipeline projects**")
        show_cols = [c for c in PIPELINE_COLS if c in cp.columns]
        st.dataframe(
            cp[show_cols].rename(columns=PIPELINE_COLS),
            use_container_width=True, hide_index=True,
        )
    else:
        st.caption("No pipeline projects for this country in the current dataset.")
