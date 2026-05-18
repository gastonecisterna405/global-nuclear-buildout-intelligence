from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method


def render(taxonomy: pd.DataFrame) -> None:
    adv = taxonomy[
        taxonomy.smr_flag.eq(True)
        | taxonomy.geniv_flag.eq(True)
        | taxonomy.thorium_potential_flag.eq(True)
    ].copy()

    if adv.empty:
        st.warning("No advanced technology records found.")
        return

    # Ensure size column has at least 1 so dots are always visible
    adv["units_uc_display"] = adv["known_under_construction_units"].clip(lower=1)

    st.markdown(
        "Each dot is a reactor type. **X** = operating units in the sample dataset. "
        "**Y** = maturity score (0–100). **Dot size** = under-construction units."
    )

    fig = px.scatter(
        adv,
        x="known_operating_units",
        y="maturity_score",
        size="units_uc_display",
        color="technology_family",
        text="reactor_type",
        hover_name="reactor_type",
        hover_data={
            "known_operating_units": True,
            "known_under_construction_units": True,
            "maturity_score": True,
            "deployment_status": True,
            "units_uc_display": False,
        },
        labels={
            "known_operating_units": "Known operating units",
            "maturity_score": "Maturity score (0–100)",
            "technology_family": "Technology family",
        },
        template="plotly_white",
        size_max=50,
    )
    fig.update_traces(
        textposition="top center",
        textfont=dict(size=10),
        marker=dict(opacity=0.85, line=dict(width=1, color="white")),
    )
    fig.update_layout(
        margin=dict(t=20, b=20),
        xaxis=dict(title="Known operating units", dtick=1, gridcolor="#f1f5f9"),
        yaxis=dict(title="Maturity score", gridcolor="#f1f5f9"),
        legend=dict(orientation="v", x=1.02, y=1),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "⚠️ Advanced technologies are scored as maturity and scenario indicators, "
        "not deterministic forecast targets. Low operating unit counts reflect "
        "real deployment gaps, not data omissions."
    )

    st.divider()
    show_cols = ["technology_family", "reactor_type", "maturity_score",
                 "commercial_maturity_level", "deployment_status",
                 "known_operating_units", "known_under_construction_units",
                 "smr_flag", "geniv_flag", "thorium_potential_flag"]
    show_cols = [c for c in show_cols if c in adv.columns]
    st.dataframe(
        adv[show_cols].sort_values("maturity_score", ascending=False),
        use_container_width=True, hide_index=True,
    )
    _method(
        data="technology_taxonomy.csv — 13 reactor types with maturity scores and deployment metadata",
        features="known_operating_units · known_under_construction_units · base_maturity · smr_flag · geniv_flag · deployment_status · coolant · neutron_spectrum",
        model="Maturity score: base_maturity + operating×1.2 + UC×1.8 (clipped 0–100)",
        notes="Score reflects deployment evidence, not vendor claims. Low unit counts = real deployment gap."
    )
