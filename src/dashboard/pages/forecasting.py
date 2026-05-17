from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(forecasts: pd.DataFrame, metrics: pd.DataFrame) -> None:
    st.plotly_chart(
        px.bar(
            forecasts, x="country", y="forecast_capacity_2035_mwe", color="region",
            title="Forecast Capacity by Country (2035)", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.caption(
        "Model target is a scenario-derived heuristic, not historical ground truth. "
        "Metrics measure fit to the heuristic rather than real-world predictive accuracy."
    )
    st.dataframe(metrics, use_container_width=True)
    st.download_button(
        "Download predictions", forecasts.to_csv(index=False), "capacity_forecasts.csv"
    )
