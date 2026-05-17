from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src import config


def render(reactors: pd.DataFrame) -> None:
    st.subheader("Data Quality & Source Coverage")

    # Missing data bar chart
    missing = (
        reactors.isna().mean()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "Field", 0: "Missing fraction"})
    )
    missing.columns = ["Field", "Missing fraction"]
    missing = missing[missing["Missing fraction"] > 0]

    st.markdown("**Missing data fraction by field**")
    if not missing.empty:
        fig = px.bar(
            missing, x="Missing fraction", y="Field",
            orientation="h",
            color="Missing fraction",
            color_continuous_scale="Reds",
            template="plotly_white",
        )
        fig.update_layout(
            margin=dict(t=10, l=10),
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed"),
            xaxis=dict(tickformat=".0%", range=[0, 1]),
            height=max(300, len(missing) * 22),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values in the current dataset.")

    # Source confidence
    st.markdown("**Source confidence by record**")
    conf = (
        reactors.groupby("source_name", as_index=False)["source_confidence"]
        .agg(avg_confidence="mean", records="count")
        .sort_values("avg_confidence", ascending=False)
        .rename(columns={"source_name": "Source",
                         "avg_confidence": "Avg confidence", "records": "Records"})
    )
    conf["Avg confidence"] = conf["Avg confidence"].round(2)
    st.dataframe(conf, use_container_width=True, hide_index=True)

    # Data sources registry
    st.markdown("**Registered data sources**")
    sources_path = config.PROCESSED / "data_sources.csv"
    if sources_path.exists():
        src = pd.read_csv(sources_path)
        show_cols = [c for c in ["source_name", "source_type", "reliability_rating",
                                  "ingestion_mode", "url", "limitations"] if c in src.columns]
        st.dataframe(src[show_cols], use_container_width=True, hide_index=True)

    st.warning(
        "Sample data is for pipeline demonstration only. "
        "Add real data via the manual templates in `data/raw/*/`."
    )
