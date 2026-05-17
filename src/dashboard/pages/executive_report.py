from __future__ import annotations

import streamlit as st

from src import config


def render() -> None:
    report_path = config.REPORTS / "global_nuclear_buildout_report.md"
    if not report_path.exists():
        st.warning("Run `python run_pipeline.py` to generate the report.")
        return

    text = report_path.read_text(encoding="utf-8")
    st.markdown(text)
    st.download_button(
        "Download markdown report", text, "global_nuclear_buildout_report.md"
    )
