from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method

STATUS_COLORS = {
    "Operating":    "#2563eb",
    "Construction": "#f59e0b",
    "Planned":      "#10b981",
    "Proposed":     "#8b5cf6",
    "Paused":       "#94a3b8",
    "Shutdown":     "#ef4444",
}

STATUS_ORDER = ["Operating", "Construction", "Planned", "Proposed", "Paused", "Shutdown"]


def _aggregate_by_plant(reactors: pd.DataFrame) -> pd.DataFrame:
    """Group individual reactor units into plant-level records for the map."""
    def primary_status(statuses: pd.Series) -> str:
        for s in STATUS_ORDER:
            if s in statuses.values:
                return s
        return statuses.iloc[0]

    plants = (
        reactors.groupby(["plant_name", "country", "region", "latitude", "longitude"])
        .agg(
            units=("reactor_id", "count"),
            total_capacity_mwe=("capacity_mwe", "sum"),
            status=("status_group", primary_status),
            technology=("technology_family", lambda s: s.mode().iloc[0] if len(s) else ""),
            reactor_types=("reactor_type_standardized", lambda s: ", ".join(sorted(s.unique()))),
        )
        .reset_index()
    )
    plants["label"] = plants.apply(
        lambda r: f"{r['plant_name']} ({int(r['units'])} unit{'s' if r['units'] > 1 else ''})", axis=1
    )
    plants["capacity_gwe"] = (plants["total_capacity_mwe"] / 1000).round(2)
    return plants


def render(reactors: pd.DataFrame) -> None:
    if reactors.empty:
        st.warning("No reactor data available.")
        return

    # --- controls ---
    col1, col2 = st.columns([3, 1])
    with col2:
        show_shutdown = st.checkbox("Show shutdown reactors", value=False)
        map_style = st.selectbox(
            "Map style",
            ["carto-positron", "carto-darkmatter", "open-street-map"],
            index=0,
        )

    df = reactors if show_shutdown else reactors[reactors.status_group != "Shutdown"]
    plants = _aggregate_by_plant(df)

    with col1:
        st.markdown(
            f"**{len(df)} reactor units** at **{len(plants)} plant sites** · "
            f"{df.country.nunique()} countries · "
            f"{df[df.status_group == 'Operating']['capacity_mwe'].sum() / 1000:,.1f} GWe operating"
        )

    # --- map ---
    fig = px.scatter_mapbox(
        plants,
        lat="latitude",
        lon="longitude",
        size="total_capacity_mwe",
        color="status",
        hover_name="label",
        hover_data={
            "country": True,
            "capacity_gwe": True,
            "units": True,
            "technology": True,
            "reactor_types": True,
            "latitude": False,
            "longitude": False,
            "total_capacity_mwe": False,
        },
        color_discrete_map=STATUS_COLORS,
        category_orders={"status": STATUS_ORDER},
        size_max=30,
        zoom=1.2,
        mapbox_style=map_style,
        labels={
            "capacity_gwe": "Capacity (GWe)",
            "units": "Units",
            "technology": "Technology",
            "reactor_types": "Reactor types",
            "status": "Status",
        },
    )
    fig.update_layout(
        height=580,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            title="Status",
            orientation="v",
            x=0.01, y=0.99,
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="#e2e8f0",
            borderwidth=1,
        ),
        mapbox=dict(center=dict(lat=30, lon=15)),
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- summary table ---
    st.divider()
    st.markdown("**Plant-level summary**")

    display = plants.rename(columns={
        "plant_name": "Plant", "country": "Country", "status": "Status",
        "units": "Units", "capacity_gwe": "GWe", "technology": "Primary technology",
        "reactor_types": "Reactor types",
    })[["Plant", "Country", "Status", "Units", "GWe", "Primary technology", "Reactor types"]]

    st.dataframe(
        display.sort_values(["Status", "GWe"], ascending=[True, False]),
        use_container_width=True,
        hide_index=True,
    )
    _method(
        data="reactors_master.csv — plant name, country, lat/lon, capacity_mwe, status_group, technology_family",
        features="Reactors aggregated by plant site (plant_name + lat/lon) · total_capacity_mwe · primary status per site",
        notes="No model — geographic aggregation and choropleth visualization."
    )
