from __future__ import annotations

import pandas as pd
import streamlit as st

from src import config


def render() -> None:
    st.write("Power BI CSV exports live in `data/powerbi/`.")

    csv_files = sorted(p.name for p in config.POWERBI.glob("*.csv"))
    st.dataframe(pd.DataFrame({"file": csv_files}), use_container_width=True)

    guide_path = config.DOCS / "powerbi_guide.md"
    if guide_path.exists():
        st.markdown(guide_path.read_text(encoding="utf-8"))
