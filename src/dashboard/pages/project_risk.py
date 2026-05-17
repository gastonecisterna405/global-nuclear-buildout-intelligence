from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(risk: pd.DataFrame) -> None:
    st.plotly_chart(
        px.scatter(
            risk,
            x="project_maturity_score", y="delay_risk_score",
            size="capacity_mwe", color="risk_level",
            hover_name="reactor_name",
            title="Project Risk Matrix", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(risk.sort_values("delay_risk_score", ascending=False), use_container_width=True)
