from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src import config


def render(reactors: pd.DataFrame) -> None:
    st.plotly_chart(
        px.imshow(reactors.isna(), title="Missingness Heatmap", aspect="auto"),
        use_container_width=True,
    )
    sources_path = config.PROCESSED / "data_sources.csv"
    if sources_path.exists():
        st.dataframe(pd.read_csv(sources_path), use_container_width=True)
    st.warning(
        "Fallback sample data is labeled sample-only. "
        "Replace or augment with official/manual source exports for production use."
    )
