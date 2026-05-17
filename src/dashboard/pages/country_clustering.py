from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(clusters: pd.DataFrame) -> None:
    st.plotly_chart(
        px.scatter(
            clusters,
            x="pca_x", y="pca_y",
            color="cluster_name", hover_name="country",
            title="Country Nuclear Strategy Clusters (PCA)", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(clusters, use_container_width=True)
