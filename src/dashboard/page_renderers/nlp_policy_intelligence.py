from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method


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
    _method(
        data="policy_documents_raw.csv (10 country policy documents) → nlp_policy_documents.csv",
        features="Raw text per document",
        model="Rule-based keyword matching across 10 topic categories (SMR, Gen IV, Financing, Delay Risk, Energy Security, Decarbonization, Fast Reactor, Molten Salt, Thorium, Industrial Heat) · NLTK tokenization + stopword removal for keyword frequency extraction",
        notes="Deterministic, auditable approach — no training data needed. Policy support signal = 20 + sum(topic_detections) × 9."
    )
