from __future__ import annotations
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src import config
from src.utils.plotting import set_theme

def _bar(df, x, y, title, filename, top=15):
    fig, ax = plt.subplots(figsize=(10, 6))
    data = df.head(top).copy()
    sns.barplot(data=data, x=x, y=y, ax=ax)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=40)
    fig.savefig(config.FIGURES / filename)
    plt.close(fig)

def generate_eda_outputs(reactors: pd.DataFrame, countries: pd.DataFrame, pipeline: pd.DataFrame, taxonomy: pd.DataFrame, scenarios: pd.DataFrame, topics: pd.DataFrame) -> None:
    set_theme()
    cap = reactors[reactors.status_group.eq("Operating")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
    _bar(cap, "country", "capacity_mwe", "Operating Nuclear Capacity by Country", "global_capacity_by_country.png")
    cnt = reactors[reactors.status_group.eq("Operating")].groupby("country", as_index=False).size().sort_values("size", ascending=False)
    _bar(cnt, "country", "size", "Operating Reactors by Country", "operating_reactors_by_country.png")
    uc = pipeline[pipeline.status_group.eq("Construction")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
    _bar(uc, "country", "capacity_mwe", "Under Construction Capacity by Country", "under_construction_by_country.png")
    planned = pipeline[pipeline.status_group.eq("Planned")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
    _bar(planned, "country", "capacity_mwe", "Planned Capacity by Country", "planned_capacity_by_country.png")
    _bar(reactors.groupby("technology_family", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False), "technology_family", "capacity_mwe", "Technology Mix - Fleet", "technology_mix_operating.png")
    _bar(pipeline.groupby("technology_family", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False), "technology_family", "capacity_mwe", "Technology Mix - Pipeline", "technology_mix_pipeline.png")
    for col, title, file in [
        ("age_years","Reactor Age Distribution","reactor_age_distribution.png"),
        ("nuclear_generation_twh","Nuclear Generation Context","nuclear_generation_trend.png"),
        ("nuclear_share_percent","Nuclear Share by Country","nuclear_share_by_country.png"),
        ("maturity_score","SMR and Gen IV Maturity Matrix","smr_geniv_maturity_matrix.png"),
    ]:
        fig, ax = plt.subplots(figsize=(10,6))
        data = taxonomy if col == "maturity_score" else countries if col in countries.columns else reactors
        sns.histplot(data[col].dropna(), ax=ax)
        ax.set_title(title)
        fig.savefig(config.FIGURES / file); plt.close(fig)
    _bar(scenarios[scenarios.year.eq(2050)].groupby("scenario", as_index=False)["capacity_gwe"].sum(), "scenario", "capacity_gwe", "2050 Capacity Scenarios", "capacity_scenarios_2050.png")
    _bar(scenarios.groupby("scenario", as_index=False)["estimated_generation_twh"].sum(), "scenario", "estimated_generation_twh", "Estimated Generation Scenarios", "estimated_generation_scenarios.png")
    _bar(countries.sort_values("policy_signal_score", ascending=False), "country", "policy_signal_score", "Country Strategy Signal", "country_strategy_clusters.png")
    fig, ax = plt.subplots(figsize=(11,6)); sns.heatmap(reactors.isna(), cbar=False, ax=ax); ax.set_title("Data Quality Heatmap"); fig.savefig(config.FIGURES / "data_quality_heatmap.png"); plt.close(fig)
    _bar(reactors.groupby("source_name", as_index=False).size(), "source_name", "size", "Source Coverage", "source_coverage_map.png")
    _bar(pipeline.groupby("expected_operation_year", as_index=False)["capacity_mwe"].sum(), "expected_operation_year", "capacity_mwe", "Pipeline Timeline", "pipeline_timeline.png")
    if (config.ANALYTICS / "nlp_keywords.csv").exists():
        kw = pd.read_csv(config.ANALYTICS / "nlp_keywords.csv").groupby("term", as_index=False)["count"].sum().sort_values("count", ascending=False)
        _bar(kw, "term", "count", "Top Policy Keywords", "top_policy_keywords.png", top=20)
    topic_heat = topics.pivot_table(index="country", columns="topic", values="present", aggfunc="max", fill_value=0)
    fig, ax = plt.subplots(figsize=(12,7)); sns.heatmap(topic_heat, annot=True, cmap="Blues", ax=ax); ax.set_title("Technology Topic Heatmap"); fig.savefig(config.FIGURES / "technology_topic_heatmap.png"); plt.close(fig)
    extra_specs = [
        ("capacity_by_region.png", reactors.groupby("region", as_index=False)["capacity_mwe"].sum(), "region", "capacity_mwe", "Capacity by Region"),
        ("pipeline_by_region.png", pipeline.groupby("country", as_index=False)["capacity_mwe"].sum(), "country", "capacity_mwe", "Pipeline by Country"),
        ("risk_by_country.png", pipeline.groupby("country", as_index=False)["delay_risk_score"].mean(), "country", "delay_risk_score", "Average Delay Risk by Country"),
        ("maturity_by_technology.png", taxonomy.sort_values("maturity_score", ascending=False), "reactor_type", "maturity_score", "Maturity by Technology"),
        ("policy_signal_by_country.png", countries.sort_values("policy_signal_score", ascending=False), "country", "policy_signal_score", "Policy Signal by Country"),
    ]
    for file, data, x, y, title in extra_specs:
        _bar(data, x, y, title, file)
    report = f'''# Full EDA Report

## Executive Readout
This EDA is generated from the processed reactor, country, pipeline, scenario and NLP tables. In this repository build, raw sample data is intentionally dirty and clearly labeled; official/manual exports can be added through the documented adapters.

## Data Quality
- Reactor rows: {len(reactors)}
- Countries represented: {reactors['country'].nunique()}
- Duplicate reactor IDs after cleaning: {reactors.duplicated('reactor_id').sum()}
- Main limitation: sample data demonstrates workflow and must not be treated as source-of-record.

## Global Fleet
Operating capacity is concentrated in countries with mature nuclear programs. The sample highlights the difference between operating capacity, under-construction capacity and early-stage planned/proposed capacity.

## Reactor Pipeline
Construction-stage projects receive higher realization scores than planned/proposed projects. Large first-of-a-kind projects and early advanced technologies receive higher delay-risk scores.

## Technology Mix
Commercial LWR families dominate maturity scoring. SMR, fast reactor, molten salt and thorium concepts are treated as strategic signals and scenario inputs, not deterministic near-term forecasts.

## Scenario Findings
The scenario engine translates capacity into TWh using capacity factor assumptions and project realization adjustments. This is a strategic planning tool, not an official forecast.

## NLP Signals
Policy text tagging detects SMR, Gen IV, financing, licensing/delay, energy security and decarbonization signals by country.
'''
    (config.OUTPUTS / "eda" / "full_eda_report.md").write_text(report, encoding="utf-8")
