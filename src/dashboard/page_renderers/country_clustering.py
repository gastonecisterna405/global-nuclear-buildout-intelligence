from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method


CLUSTER_COLORS = {
    "Mature or legacy fleet":    "#2563eb",
    "High-growth builder":       "#f59e0b",
    "Emerging nuclear entrant":  "#10b981",
    "Advanced technology explorer": "#8b5cf6",
    "Nuclear strategy segment":  "#94a3b8",
}


def render(clusters: pd.DataFrame) -> None:
    if clusters.empty:
        st.warning("Cluster data missing. Run `python run_pipeline.py`.")
        return

    st.markdown(
        "Countries projected into 2D using PCA on nuclear fleet, pipeline, "
        "demand, GDP and policy features. Hover for details."
    )

    fig = px.scatter(
        clusters,
        x="pca_x", y="pca_y",
        color="cluster_name",
        text="country",
        hover_name="country",
        hover_data={"pca_x": False, "pca_y": False,
                    "cluster_id": False, "region": True},
        color_discrete_map=CLUSTER_COLORS,
        labels={"pca_x": "PC 1", "pca_y": "PC 2", "cluster_name": "Cluster"},
        template="plotly_white",
    )
    fig.update_traces(
        textposition="top center",
        textfont=dict(size=11, color="#1e293b"),
        marker=dict(size=14, opacity=0.85,
                    line=dict(width=1.5, color="white")),
    )
    fig.update_layout(
        height=520,
        margin=dict(t=20, b=20),
        xaxis=dict(title="PC 1 (primary variance)", gridcolor="#f1f5f9",
                   zeroline=True, zerolinecolor="#e2e8f0"),
        yaxis=dict(title="PC 2 (secondary variance)", gridcolor="#f1f5f9",
                   zeroline=True, zerolinecolor="#e2e8f0"),
        legend=dict(title="Cluster", orientation="v", x=1.02, y=1),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Cluster summary table
    st.markdown("**Countries by cluster**")
    summary = (
        clusters.groupby("cluster_name")["country"]
        .apply(lambda s: ", ".join(sorted(s)))
        .reset_index()
        .rename(columns={"cluster_name": "Cluster", "country": "Countries"})
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)
    _method(
        data="country_nuclear_profile.csv (34 country profiles)",
        features="operating/construction/planned/proposed capacity · nuclear share % · GDP · electricity generation · population · average fleet age · advanced_reactor_activity_score · policy_signal_score (11 features)",
        model="KMeans clustering (k=3, n_init=10) · PCA (2 components) for visualization. StandardScaler applied before both. Silhouette score used to select k.",
        notes="Cluster names are interpretive labels assigned post-hoc. With 34 countries, clusters reflect structural differences in nuclear strategy."
    )
