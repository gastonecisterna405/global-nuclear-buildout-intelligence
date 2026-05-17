import streamlit as st

def apply_style() -> None:
    st.markdown('''
    <style>
    :root {
        color-scheme: light;
    }

    .stApp {
        background: #f5f7fb;
        color: #17202a;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .gnbi-header {
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: .8rem;
        margin-bottom: 1.2rem;
    }

    .gnbi-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: 0;
    }

    .gnbi-subtitle {
        font-size: 1rem;
        color: #475569;
        margin-top: .25rem;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #d8e0ea;
        padding: .85rem .95rem;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, .05);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] div {
        color: #0f172a !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: .84rem;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.55rem;
        font-weight: 800;
    }

    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 8px;
    }

    .stAlert {
        color: #0f172a;
    }

    h1, h2, h3, h4, h5, h6, p, label, span {
        color: inherit;
    }

    .small-note {
        font-size: .82rem;
        color: #64748b;
    }
    </style>
    ''', unsafe_allow_html=True)
