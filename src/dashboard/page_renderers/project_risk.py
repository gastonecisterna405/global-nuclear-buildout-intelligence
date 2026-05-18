from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method


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
    _method(
        data="reactor_pipeline.csv (UC/Planned/Proposed projects with scoring features)",
        features="status_group · technology_family · reactor_type · capacity_mwe · project_maturity_score · delay_risk_score (6 features)",
        model="Logistic Regression · Random Forest (n=120) · XGBoost (n=60, depth=3) — binary classification of high vs low realization probability. Best model selected by F1.",
        notes="Labels derived from scoring heuristic (no historical realization data). Models demonstrate the sklearn pipeline pattern rather than predictive validity."
    )
