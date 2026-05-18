from __future__ import annotations

import streamlit as st


def section(
    data: str,
    features: str | None = None,
    model: str | None = None,
    notes: str | None = None,
) -> None:
    """Render a collapsible methodology section at the bottom of a dashboard page."""
    with st.expander("Methodology — data, features & model", expanded=False):
        st.markdown(f"**Data used:** {data}")
        if features:
            st.markdown(f"**Features:** {features}")
        if model:
            st.markdown(f"**Model:** {model}")
        if notes:
            st.caption(notes)
