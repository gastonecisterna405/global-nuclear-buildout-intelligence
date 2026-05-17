from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


def render(docs: pd.DataFrame) -> None:
    if docs.empty:
        st.warning("NLP outputs missing. Run the pipeline to generate them.")
        return

    st.plotly_chart(
        px.bar(
            docs, x="country", y="policy_support_signal", color="detected_topics",
            title="Policy Signal Score by Country", template="plotly_white",
        ),
        use_container_width=True,
    )
    st.dataframe(docs, use_container_width=True)
