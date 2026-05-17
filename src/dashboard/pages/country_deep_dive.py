from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(
    reactors: pd.DataFrame,
    countries: pd.DataFrame,
    pipeline: pd.DataFrame,
) -> None:
    selected = st.selectbox("Select country", sorted(countries.country.dropna().unique()))

    cr = reactors[reactors.country == selected]
    cp = pipeline[pipeline.country == selected]

    st.subheader(selected)
    st.dataframe(countries[countries.country == selected], use_container_width=True)

    left, right = st.columns(2)
    left.plotly_chart(
        px.bar(
            cr.groupby("status_group", as_index=False)["capacity_mwe"].sum(),
            x="status_group", y="capacity_mwe",
            title="Fleet and Pipeline Status", template="plotly_white",
        ),
        use_container_width=True,
    )
    right.plotly_chart(
        px.bar(
            cr.groupby("technology_family", as_index=False)["capacity_mwe"].sum(),
            x="technology_family", y="capacity_mwe",
            title="Technology Mix", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(cp, use_container_width=True)
