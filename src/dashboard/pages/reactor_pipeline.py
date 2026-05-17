from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(pipeline: pd.DataFrame) -> None:
    st.plotly_chart(
        px.bar(
            pipeline.groupby("expected_operation_year", as_index=False)["capacity_mwe"].sum(),
            x="expected_operation_year", y="capacity_mwe",
            title="Expected Pipeline Additions by Year", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.plotly_chart(
        px.histogram(
            pipeline, x="status_group", color="technology_family",
            title="Pipeline Funnel by Technology", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(pipeline, use_container_width=True)
