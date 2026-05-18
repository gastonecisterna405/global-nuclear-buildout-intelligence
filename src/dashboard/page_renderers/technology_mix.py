from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method


def render(reactors: pd.DataFrame, taxonomy: pd.DataFrame) -> None:
    left, right = st.columns(2)
    left.plotly_chart(
        px.pie(
            reactors, names="reactor_type_standardized", values="capacity_mwe",
            title="Fleet Reactor Type Mix",
        ),
        use_container_width=True,
    )
    right.plotly_chart(
        px.bar(
            taxonomy, x="reactor_type", y="maturity_score", color="technology_family",
            title="Technology Maturity Score", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(taxonomy, use_container_width=True)
    _method(
        data="reactors_master.csv (fleet) · reactor_pipeline.csv (pipeline) · technology_taxonomy.csv (maturity scores)",
        features="technology_family · reactor_type_standardized · capacity_mwe by status group",
        model="Technology maturity score: base_maturity + operating_units×1.2 + UC_units×1.8 · Trained Random Forest on taxonomy features to reproduce score (demo of sklearn pipeline pattern)",
        notes="Maturity score combines public deployment status, unit counts, novelty and regulatory familiarity."
    )
