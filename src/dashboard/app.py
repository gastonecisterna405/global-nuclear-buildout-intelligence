from __future__ import annotations
from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src import config
from src.dashboard.components.styling import apply_style

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

st.markdown('<div class="gnbi-header"><div class="gnbi-title">GLOBAL NUCLEAR BUILDOUT INTELLIGENCE PLATFORM</div><div class="gnbi-subtitle">Reactor Pipeline Forecasting, Technology Mix Scoring & Nuclear Electricity Supply Scenarios</div></div>', unsafe_allow_html=True)
if reactors.empty:
    st.warning("Processed files are missing. Run `python run_pipeline.py` from the project root.")
    st.stop()

st.sidebar.header("Global Filters")
country_filter = st.sidebar.multiselect("Country", sorted(reactors.country.dropna().unique()), default=sorted(reactors.country.dropna().unique()))
region_filter = st.sidebar.multiselect("Region", sorted(reactors.region.dropna().unique()), default=sorted(reactors.region.dropna().unique()))
status_filter = st.sidebar.multiselect("Status group", sorted(reactors.status_group.dropna().unique()), default=sorted(reactors.status_group.dropna().unique()))
tech_filter = st.sidebar.multiselect("Technology family", sorted(reactors.technology_family.dropna().unique()), default=sorted(reactors.technology_family.dropna().unique()))
scenario_filter = st.sidebar.selectbox("Scenario", sorted(scenarios.scenario.dropna().unique()) if not scenarios.empty else ["Base"], index=0)
capacity_factor = st.sidebar.slider("Capacity factor", 0.50, 0.95, 0.86, 0.01)
price = st.sidebar.slider("Price per MWh", 20, 200, 75, 5)
realization_adjustment = st.sidebar.slider("Project realization adjustment", 0.25, 1.25, 1.00, 0.05)

r = reactors[reactors.country.isin(country_filter) & reactors.region.isin(region_filter) & reactors.status_group.isin(status_filter) & reactors.technology_family.isin(tech_filter)]
p = pipeline[pipeline.country.isin(country_filter)] if not pipeline.empty else pipeline
c = countries[countries.country.isin(country_filter)] if not countries.empty else countries

pages = [
    "Executive Overview", "Global Nuclear Map", "Country Deep Dive", "Reactor Pipeline",
    "Technology Mix", "SMR / Gen IV / Thorium Watch", "Forecasting", "Project Risk Scoring",
    "Electricity Supply Scenarios", "Country Strategy Clustering", "NLP / Policy Intelligence",
    "Data Quality & Source Coverage", "Executive Report", "Power BI Export"
]
page = st.sidebar.radio("Page", pages)

if page == "Executive Overview":
    cols = st.columns(4)
    cols[0].metric("Operating reactors", int((r.status_group == "Operating").sum()))
    cols[1].metric("Operating capacity", f"{r.loc[r.status_group=='Operating','capacity_mwe'].sum()/1000:,.1f} GWe")
    cols[2].metric("Under construction", int((r.status_group == "Construction").sum()))
    cols[3].metric("Construction capacity", f"{r.loc[r.status_group=='Construction','capacity_mwe'].sum()/1000:,.1f} GWe")
    cols = st.columns(4)
    cols[0].metric("Planned capacity", f"{r.loc[r.status_group=='Planned','capacity_mwe'].sum()/1000:,.1f} GWe")
    cols[1].metric("Proposed capacity", f"{r.loc[r.status_group=='Proposed','capacity_mwe'].sum()/1000:,.1f} GWe")
    cols[2].metric("Countries with nuclear records", r.country.nunique())
    cols[3].metric("2050 scenario TWh", f"{scenarios[(scenarios.year==2050)&(scenarios.scenario==scenario_filter)].estimated_generation_twh.sum():,.0f}")
    left, right = st.columns([1.2, 1])
    with left:
        cap = r.groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False).head(12)
        st.plotly_chart(px.bar(cap, x="country", y="capacity_mwe", title="Capacity by Country", template="plotly_white"), use_container_width=True)
    with right:
        st.info("Generated insight: construction-stage projects and mature LWR technologies drive near-term capacity confidence. SMR and Gen IV concepts are best read as strategic signals until deployment history improves.")
        st.dataframe(p.sort_values("realization_probability", ascending=False).head(5), use_container_width=True)

elif page == "Global Nuclear Map":
    st.plotly_chart(px.scatter_geo(r, lat="latitude", lon="longitude", size="capacity_mwe", color="status_group", hover_name="reactor_name", hover_data=["country","reactor_type_standardized","technology_family","source_name"], projection="natural earth", title="Global Reactor / Project Map", template="plotly_white"), use_container_width=True)
    st.dataframe(r, use_container_width=True)

elif page == "Country Deep Dive":
    selected = st.selectbox("Select country", sorted(countries.country.dropna().unique()))
    cr = reactors[reactors.country == selected]
    cp = pipeline[pipeline.country == selected]
    st.subheader(selected)
    st.dataframe(countries[countries.country == selected], use_container_width=True)
    a, b = st.columns(2)
    a.plotly_chart(px.bar(cr.groupby("status_group", as_index=False)["capacity_mwe"].sum(), x="status_group", y="capacity_mwe", title="Fleet and Pipeline Status", template="plotly_white"), use_container_width=True)
    b.plotly_chart(px.bar(cr.groupby("technology_family", as_index=False)["capacity_mwe"].sum(), x="technology_family", y="capacity_mwe", title="Technology Mix", template="plotly_white"), use_container_width=True)
    st.dataframe(cp, use_container_width=True)

elif page == "Reactor Pipeline":
    st.plotly_chart(px.bar(p.groupby("expected_operation_year", as_index=False)["capacity_mwe"].sum(), x="expected_operation_year", y="capacity_mwe", title="Expected Pipeline Additions", template="plotly_white"), use_container_width=True)
    st.plotly_chart(px.histogram(p, x="status_group", color="technology_family", title="Pipeline Funnel", template="plotly_white"), use_container_width=True)
    st.dataframe(p, use_container_width=True)

elif page == "Technology Mix":
    a, b = st.columns(2)
    a.plotly_chart(px.pie(r, names="reactor_type_standardized", values="capacity_mwe", title="Fleet Reactor Type Mix"), use_container_width=True)
    b.plotly_chart(px.bar(taxonomy, x="reactor_type", y="maturity_score", color="technology_family", title="Technology Maturity", template="plotly_white"), use_container_width=True)
    st.dataframe(taxonomy, use_container_width=True)

elif page == "SMR / Gen IV / Thorium Watch":
    adv = taxonomy[(taxonomy.smr_flag == True) | (taxonomy.geniv_flag == True) | (taxonomy.thorium_potential_flag == True)]
    st.plotly_chart(px.scatter(adv, x="known_operating_units", y="maturity_score", size="known_under_construction_units", color="technology_family", hover_name="reactor_type", title="Maturity vs Deployment Reality", template="plotly_white"), use_container_width=True)
    st.warning("Advanced technologies are scored as maturity and scenario indicators, not deterministic forecast targets.")
    st.dataframe(adv, use_container_width=True)

elif page == "Forecasting":
    st.plotly_chart(px.bar(forecasts, x="country", y="forecast_capacity_2035_mwe", color="region", title="Forecast Capacity by Country", template="plotly_white"), use_container_width=True)
    st.dataframe(metrics, use_container_width=True)
    st.download_button("Download predictions", forecasts.to_csv(index=False), "capacity_forecasts.csv")

elif page == "Project Risk Scoring":
    st.plotly_chart(px.scatter(risk, x="project_maturity_score", y="delay_risk_score", size="capacity_mwe", color="risk_level", hover_name="reactor_name", title="Project Risk Matrix", template="plotly_white"), use_container_width=True)
    st.dataframe(risk.sort_values("delay_risk_score", ascending=False), use_container_width=True)

elif page == "Electricity Supply Scenarios":
    s = scenarios[scenarios.scenario == scenario_filter].copy()
    s["estimated_generation_twh_adjusted"] = s.capacity_gwe * capacity_factor * 8.76 * realization_adjustment
    s["estimated_market_value_usd"] = s.estimated_generation_twh_adjusted * 1_000_000 * price
    st.metric("Estimated scenario generation", f"{s.estimated_generation_twh_adjusted.sum():,.0f} TWh/year")
    st.metric("Estimated market value proxy", f"${s.estimated_market_value_usd.sum()/1e9:,.1f}B")
    st.plotly_chart(px.line(s.groupby("year", as_index=False)["estimated_generation_twh_adjusted"].sum(), x="year", y="estimated_generation_twh_adjusted", title="Scenario Generation Sensitivity", template="plotly_white"), use_container_width=True)
    st.dataframe(s, use_container_width=True)

elif page == "Country Strategy Clustering":
    st.plotly_chart(px.scatter(clusters, x="pca_x", y="pca_y", color="cluster_name", hover_name="country", title="Country Nuclear Strategy Clusters", template="plotly_white"), use_container_width=True)
    st.dataframe(clusters, use_container_width=True)

elif page == "NLP / Policy Intelligence":
    if docs.empty:
        st.warning("NLP outputs missing.")
    else:
        st.plotly_chart(px.bar(docs, x="country", y="policy_support_signal", color="detected_topics", title="Policy Signal Score", template="plotly_white"), use_container_width=True)
        st.dataframe(docs, use_container_width=True)

elif page == "Data Quality & Source Coverage":
    st.plotly_chart(px.imshow(reactors.isna(), title="Missingness Heatmap", aspect="auto"), use_container_width=True)
    st.dataframe(load_csv(config.PROCESSED / "data_sources.csv"), use_container_width=True)
    st.warning("Fallback sample data is labeled sample-only. Replace or augment it with official/manual source exports for production use.")

elif page == "Executive Report":
    report_path = config.REPORTS / "global_nuclear_buildout_report.md"
    text = report_path.read_text(encoding="utf-8") if report_path.exists() else "Run the pipeline to generate the report."
    st.markdown(text)
    st.download_button("Download markdown report", text, "global_nuclear_buildout_report.md")

elif page == "Power BI Export":
    st.write("Power BI CSV exports live in `data/powerbi/`.")
    st.dataframe(pd.DataFrame({"file": sorted([p.name for p in config.POWERBI.glob("*.csv")])}), use_container_width=True)
    st.markdown(Path(config.DOCS / "powerbi_guide.md").read_text(encoding="utf-8") if (config.DOCS / "powerbi_guide.md").exists() else "")
