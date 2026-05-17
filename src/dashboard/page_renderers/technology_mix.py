from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


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
