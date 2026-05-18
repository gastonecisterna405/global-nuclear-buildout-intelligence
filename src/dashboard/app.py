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
from src.dashboard.page_renderers import (
    country_clustering,
    country_deep_dive,
    data_quality,
    electricity_scenarios,
    executive_overview,
    executive_report,
    forecasting,
    full_eda,
    global_map,
    nlp_policy_intelligence,
    powerbi_export,
    project_risk,
    reactor_pipeline,
    smr_geniv_watch,
    technology_mix,
)

st.set_page_config(
    page_title="Global Nuclear Buildout Intelligence",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_style()


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


reactors  = load_csv(config.PROCESSED / "reactors_master.csv")
countries = load_csv(config.PROCESSED / "country_nuclear_profile.csv")
pipeline  = load_csv(config.PROCESSED / "reactor_pipeline.csv")
taxonomy  = load_csv(config.PROCESSED / "technology_taxonomy.csv")
scenarios = load_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv")
forecasts = load_csv(config.PREDICTIONS / "capacity_forecasts.csv")
risk      = load_csv(config.PREDICTIONS / "project_risk_scores.csv")
clusters  = load_csv(config.PREDICTIONS / "country_clusters.csv")
docs      = load_csv(config.PROCESSED / "nlp_policy_documents.csv")
metrics   = load_csv(config.PROCESSED / "model_metrics.csv")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="gnbi-header">'
    "<div class=\"gnbi-title\">Global Nuclear Buildout Intelligence</div>"
    '<div class="gnbi-subtitle">'
    "Reactor Pipeline · Technology Maturity · Project Risk · Electricity Scenarios"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

if reactors.empty:
    st.warning("Processed files missing. Run `python run_pipeline.py` first.")
    st.stop()

st.info(
    "**Curated sample dataset** — based on IAEA PRIS / WNA / GEM public records "
    f"({len(reactors)} reactor units, {reactors.country.nunique()} countries). "
    "Numbers are representative but not a source-of-record. "
    "See *Data Quality* for how to substitute official exports.",
    icon=None,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Navigation")

PAGES = [
    "Executive Overview",
    "Full EDA",
    "Global Nuclear Map",
    "Country Deep Dive",
    "Reactor Pipeline",
    "Technology Mix",
    "SMR / Gen IV Watch",
    "Forecasting",
    "Project Risk Scoring",
    "Electricity Scenarios",
    "Country Clustering",
    "NLP / Policy Intelligence",
    "Data Quality",
    "Executive Report",
    "Power BI Export",
]
page = st.sidebar.radio("", PAGES, label_visibility="collapsed")

st.sidebar.divider()
st.sidebar.subheader("Filters")
st.sidebar.caption("Leave empty to include all.")

country_opts  = sorted(reactors.country.dropna().unique())
region_opts   = sorted(reactors.region.dropna().unique())
status_opts   = sorted(reactors.status_group.dropna().unique())
tech_opts     = sorted(reactors.technology_family.dropna().unique())
scenario_opts = sorted(scenarios.scenario.dropna().unique()) if not scenarios.empty else ["Base"]

region_sel  = st.sidebar.multiselect("Region",     region_opts,  placeholder="All regions")
status_sel  = st.sidebar.multiselect("Status",     status_opts,  placeholder="All statuses")
country_sel = st.sidebar.multiselect("Country",    country_opts, placeholder="All countries")

with st.sidebar.expander("Scenario & model settings"):
    tech_sel        = st.multiselect("Technology", tech_opts, placeholder="All technologies")
    scenario_filter = st.selectbox("Scenario", scenario_opts)
    capacity_factor = st.slider("Capacity factor", 0.50, 0.95, 0.86, 0.01)
    price           = st.slider("Price per MWh ($)", 20, 200, 75, 5)
    realization_adjustment = st.slider("Realization adjustment", 0.25, 1.25, 1.00, 0.05)

# Empty selection means "all"
region_filter  = region_sel  or region_opts
status_filter  = status_sel  or status_opts
country_filter = country_sel or country_opts
tech_filter    = tech_sel    or tech_opts

# Filtered views
r = reactors[
    reactors.country.isin(country_filter)
    & reactors.region.isin(region_filter)
    & reactors.status_group.isin(status_filter)
    & reactors.technology_family.isin(tech_filter)
]
p = pipeline[pipeline.country.isin(country_filter)] if not pipeline.empty else pipeline
c = countries[countries.country.isin(country_filter)] if not countries.empty else countries

# ── Page routing ──────────────────────────────────────────────────────────────
if "Executive Overview" in page:
    executive_overview.render(r, p, scenarios, scenario_filter)

elif "Full EDA" in page:
    full_eda.render(r, c, p, taxonomy)

elif "Global Nuclear Map" in page:
    global_map.render(r)

elif "Country Deep Dive" in page:
    country_deep_dive.render(r, c, p)

elif "Reactor Pipeline" in page:
    reactor_pipeline.render(p)

elif "Technology Mix" in page:
    technology_mix.render(r, taxonomy)

elif "SMR" in page:
    smr_geniv_watch.render(taxonomy)

elif "Forecasting" in page:
    forecasting.render(forecasts, metrics)

elif "Project Risk" in page:
    project_risk.render(risk)

elif "Electricity" in page:
    electricity_scenarios.render(scenarios, scenario_filter, capacity_factor, price, realization_adjustment)

elif "Clustering" in page:
    country_clustering.render(clusters)

elif "Policy" in page:
    nlp_policy_intelligence.render(docs)

elif "Data Quality" in page:
    data_quality.render(r)

elif "Executive Report" in page:
    executive_report.render()

elif "Power BI" in page:
    powerbi_export.render()
