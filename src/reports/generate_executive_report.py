from __future__ import annotations
import os
import pandas as pd
from src import config

DISCLAIMER = "This is a strategic analytics tool, not an official forecast or investment recommendation."

def generate_executive_report() -> str:
    reactors = pd.read_csv(config.PROCESSED / "reactors_master.csv")
    countries = pd.read_csv(config.PROCESSED / "country_nuclear_profile.csv")
    pipeline = pd.read_csv(config.PROCESSED / "reactor_pipeline.csv")
    taxonomy = pd.read_csv(config.PROCESSED / "technology_taxonomy.csv")
    scenarios = pd.read_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv")
    risk = pd.read_csv(config.PREDICTIONS / "project_risk_scores.csv")
    top_growth = pipeline.groupby("country")["capacity_mwe"].sum().sort_values(ascending=False).head(5)
    report = f'''# Global Nuclear Buildout Intelligence Report

## 1. Executive Summary
The platform integrates reactor, country, technology, pipeline, scenario and policy-text analytics to evaluate where nuclear capacity may grow and what strategic risks affect the buildout. {DISCLAIMER}

## 2. Global Nuclear Buildout Overview
- Processed reactor/unit records: {len(reactors)}
- Countries represented: {reactors.country.nunique()}
- Operating capacity in processed table: {reactors.loc[reactors.status_group.eq("Operating"), "capacity_mwe"].sum():,.0f} MWe
- Construction capacity in processed table: {reactors.loc[reactors.status_group.eq("Construction"), "capacity_mwe"].sum():,.0f} MWe

## 3. Reactor Pipeline Analysis
Top pipeline countries by capacity: {", ".join([f"{c} ({v:,.0f} MWe)" for c, v in top_growth.items()])}.

## 4. Technology Mix Analysis
Commercial LWR technologies receive the highest maturity scores. Advanced reactor families are retained as scenario and maturity signals unless real deployment evidence supports forecasting.

## 5. SMR and Gen IV Watch
SMR/Gen IV scoring combines deployment stage, units operating/under construction, novelty, fuel/coolant complexity and source confidence. This avoids overstating early-stage technology certainty.

## 6. Country Strategy Clusters
Country clustering segments markets by operating capacity, pipeline, nuclear share, demand context, advanced-reactor activity and policy signal.

## 7. Forecasting Results
The forecasting table estimates near/mid-term capacity using pipeline and country features. It is a model demonstration and should be retrained with historical snapshots for production use.

## 8. Electricity Supply Scenarios
The scenario engine uses TWh/year = capacity_GW * capacity_factor * 8.76 and exposes capacity factor, realization probability and price assumptions.

## 9. Project Risk and Delay Analysis
Projects are scored with a transparent decision-support approach. High realization probabilities generally reflect construction status, mature technology and experienced nuclear countries.

## 10. Policy and NLP Signals
NLP tagging extracts signals for SMR, Gen IV, financing, licensing, energy security, decarbonization and industrial heat from curated public-text samples.

## 11. Business / Strategic Implications
The platform supports market screening, pipeline diligence, technology strategy, scenario planning and stakeholder reporting.

## 12. Data Limitations
Public nuclear data is fragmented. Planned/proposed project dates and advanced reactor deployment claims require careful source review. Sample data is not a source-of-record.

## 13. Recommended Next Steps
Replace sample rows with official/manual exports, add time-stamped project snapshots, validate risk labels against historical outcomes and connect Power BI/Streamlit to scheduled data refresh.

Sources used by this generated report: processed source registry, reactor master table, technology taxonomy, pipeline table, scenario table and NLP policy table.
'''
    path = config.REPORTS / "global_nuclear_buildout_report.md"
    path.write_text(report, encoding="utf-8")
    (config.REPORTS / "executive_summary.md").write_text(report.split("## 2.")[0], encoding="utf-8")
    return report
