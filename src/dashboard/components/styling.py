import streamlit as st


def apply_style() -> None:
    st.markdown("""
    <style>
    :root { color-scheme: light; }

    .stApp {
        background: #f0f4f8;
        color: #1a202c;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1400px;
    }

    /* ── Header ── */
    .gnbi-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
        border-radius: 10px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.4rem;
    }
    .gnbi-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.3px;
    }
    .gnbi-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        letter-spacing: 0.4px;
    }

    /* ── Metric cards ── */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,.06);
    }
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: .82rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #1e293b;
    }
    section[data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 0.9rem;
        padding: 2px 0;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #334155;
    }

    /* ── DataFrames ── */
    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }

    /* ── Info/warning banners ── */
    div[data-testid="stInfo"] {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        color: #1e40af;
        border-radius: 0 6px 6px 0;
    }

    h1, h2, h3 { color: #0f172a; }
    </style>
    """, unsafe_allow_html=True)
