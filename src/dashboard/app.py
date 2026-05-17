from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import config
from src.dashboard.components.styling import apply_style
from src.dashboard.pages import (
    country_clustering,
    country_deep_dive,
    data_quality,
    electricity_scenarios,
    executive_overview,
    executive_report,
    forecasting,
    global_map,
    nlp_policy_intelligence,
    powerbi_export,
    project_risk,
    reactor_pipeline,
    smr_geniv_watch,
    technology_mix,
)

st.set_page_config(page_title="Global Nuclear Buildout Intelligence", layout="wide")
apply_style()


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


reactors = load_csv(config.PROCESSED / "reactors_master.csv")
countries = load_csv(config.PROCESSED / "country_nuclear_profile.csv")
pipeline = load_csv(config.PROCESSED / "reactor_pipeline.csv")
taxonomy = load_csv(config.PROCESSED / "technology_taxonomy.csv")
scenarios = load_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv")
forecasts = load_csv(config.PREDICTIONS / "capacity_forecasts.csv")
risk = load_csv(config.PREDICTIONS / "project_risk_scores.csv")
clusters = load_csv(config.PREDICTIONS / "country_clusters.csv")
docs = load_csv(config.PROCESSED / "nlp_policy_documents.csv")
metrics = load_csv(config.PROCESSED / "model_metrics.csv")

st.markdown(
    '<div class="gnbi-header">'
    '<div class="gnbi-title">GLOBAL NUCLEAR BUILDOUT INTELLIGENCE PLATFORM</div>'
    '<div class="gnbi-subtitle">Reactor Pipeline Forecasting, Technology Mix Scoring &amp; '
    "Nuclear Electricity Supply Scenarios</div>"
    "</div>",
    unsafe_allow_html=True,
)

if reactors.empty:
    st.warning("Processed files are missing. Run `python run_pipeline.py` from the project root.")
    st.stop()

# --- Sidebar filters ---
st.sidebar.header("Global Filters")

country_opts = sorted(reactors.country.dropna().unique())
region_opts = sorted(reactors.region.dropna().unique())
status_opts = sorted(reactors.status_group.dropna().unique())
tech_opts = sorted(reactors.technology_family.dropna().unique())
scenario_opts = sorted(scenarios.scenario.dropna().unique()) if not scenarios.empty else ["Base"]

country_filter = st.sidebar.multiselect("Country", country_opts, default=country_opts)
region_filter = st.sidebar.multiselect("Region", region_opts, default=region_opts)
status_filter = st.sidebar.multiselect("Status group", status_opts, default=status_opts)
tech_filter = st.sidebar.multiselect("Technology family", tech_opts, default=tech_opts)
scenario_filter = st.sidebar.selectbox("Scenario", scenario_opts)
capacity_factor = st.sidebar.slider("Capacity factor", 0.50, 0.95, 0.86, 0.01)
price = st.sidebar.slider("Price per MWh ($)", 20, 200, 75, 5)
realization_adjustment = st.sidebar.slider("Project realization adjustment", 0.25, 1.25, 1.00, 0.05)

# Filtered views
r = reactors[
    reactors.country.isin(country_filter)
    & reactors.region.isin(region_filter)
    & reactors.status_group.isin(status_filter)
    & reactors.technology_family.isin(tech_filter)
]
p = pipeline[pipeline.country.isin(country_filter)] if not pipeline.empty else pipeline
c = countries[countries.country.isin(country_filter)] if not countries.empty else countries

# --- Page routing ---
PAGES = [
    "Executive Overview",
    "Global Nuclear Map",
    "Country Deep Dive",
    "Reactor Pipeline",
    "Technology Mix",
    "SMR / Gen IV / Thorium Watch",
    "Forecasting",
    "Project Risk Scoring",
    "Electricity Supply Scenarios",
    "Country Strategy Clustering",
    "NLP / Policy Intelligence",
    "Data Quality & Source Coverage",
    "Executive Report",
    "Power BI Export",
]
page = st.sidebar.radio("Page", PAGES)

if page == "Executive Overview":
    executive_overview.render(r, p, scenarios, scenario_filter)

elif page == "Global Nuclear Map":
    global_map.render(r)

elif page == "Country Deep Dive":
    country_deep_dive.render(r, c, p)

elif page == "Reactor Pipeline":
    reactor_pipeline.render(p)

elif page == "Technology Mix":
    technology_mix.render(r, taxonomy)

elif page == "SMR / Gen IV / Thorium Watch":
    smr_geniv_watch.render(taxonomy)

elif page == "Forecasting":
    forecasting.render(forecasts, metrics)

elif page == "Project Risk Scoring":
    project_risk.render(risk)

elif page == "Electricity Supply Scenarios":
    electricity_scenarios.render(scenarios, scenario_filter, capacity_factor, price, realization_adjustment)

elif page == "Country Strategy Clustering":
    country_clustering.render(clusters)

elif page == "NLP / Policy Intelligence":
    nlp_policy_intelligence.render(docs)

elif page == "Data Quality & Source Coverage":
    data_quality.render(r)

elif page == "Executive Report":
    executive_report.render()

elif page == "Power BI Export":
    powerbi_export.render()
