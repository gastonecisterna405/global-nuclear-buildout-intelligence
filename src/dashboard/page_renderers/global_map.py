from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(reactors: pd.DataFrame) -> None:
    st.plotly_chart(
        px.scatter_geo(
            reactors,
            lat="latitude", lon="longitude",
            size="capacity_mwe", color="status_group",
            hover_name="reactor_name",
            hover_data=["country", "reactor_type_standardized", "technology_family", "source_name"],
            projection="natural earth",
            title="Global Reactor / Project Map",
            template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(reactors, use_container_width=True)
