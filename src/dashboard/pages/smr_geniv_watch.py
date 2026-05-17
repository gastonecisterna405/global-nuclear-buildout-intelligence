from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(taxonomy: pd.DataFrame) -> None:
    adv = taxonomy[
        taxonomy.smr_flag.eq(True)
        | taxonomy.geniv_flag.eq(True)
        | taxonomy.thorium_potential_flag.eq(True)
    ]
    st.plotly_chart(
        px.scatter(
            adv,
            x="known_operating_units", y="maturity_score",
            size="known_under_construction_units", color="technology_family",
            hover_name="reactor_type",
            title="Maturity vs Deployment Reality", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.warning(
        "Advanced technologies are scored as maturity and scenario indicators, "
        "not deterministic forecast targets."
    )
    st.dataframe(adv, use_container_width=True)
