from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src import config
from src.utils.plotting import set_theme


def _bar(df: pd.DataFrame, x: str, y: str, title: str, filename: str, top: int = 15) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df.head(top), x=x, y=y, ax=ax)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=40)
    fig.savefig(config.FIGURES / filename)
    plt.close(fig)


def _hist(df: pd.DataFrame, col: str, title: str, filename: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[col].dropna(), ax=ax)
    ax.set_title(title)
    fig.savefig(config.FIGURES / filename)
    plt.close(fig)


def generate_eda_outputs(
    reactors: pd.DataFrame,
    countries: pd.DataFrame,
    pipeline: pd.DataFrame,
    taxonomy: pd.DataFrame,
    scenarios: pd.DataFrame,
    topics: pd.DataFrame,
) -> None:
    set_theme()

    # --- Fleet charts ---
    cap = (
        reactors[reactors.status_group == "Operating"]
        .groupby("country", as_index=False)["capacity_mwe"]
        .sum()
        .sort_values("capacity_mwe", ascending=False)
    )
    _bar(cap, "country", "capacity_mwe", "Operating Nuclear Capacity by Country", "global_capacity_by_country.png")

    cnt = (
        reactors[reactors.status_group == "Operating"]
        .groupby("country", as_index=False)
        .size()
        .sort_values("size", ascending=False)
    )
    _bar(cnt, "country", "size", "Operating Reactors by Country", "operating_reactors_by_country.png")

    # --- Pipeline charts ---
    uc = (
        pipeline[pipeline.status_group == "Construction"]
        .groupby("country", as_index=False)["capacity_mwe"]
        .sum()
        .sort_values("capacity_mwe", ascending=False)
    )
    _bar(uc, "country", "capacity_mwe", "Under Construction Capacity by Country", "under_construction_by_country.png")

    planned = (
        pipeline[pipeline.status_group == "Planned"]
        .groupby("country", as_index=False)["capacity_mwe"]
        .sum()
        .sort_values("capacity_mwe", ascending=False)
    )
    _bar(planned, "country", "capacity_mwe", "Planned Capacity by Country", "planned_capacity_by_country.png")

    _bar(
        pipeline.groupby("expected_operation_year", as_index=False)["capacity_mwe"].sum(),
        "expected_operation_year", "capacity_mwe",
        "Pipeline Expected Additions by Year", "pipeline_timeline.png",
    )

    # --- Technology charts ---
    _bar(
        reactors.groupby("technology_family", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False),
        "technology_family", "capacity_mwe", "Technology Mix – Operating Fleet", "technology_mix_operating.png",
    )
    _bar(
        pipeline.groupby("technology_family", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False),
        "technology_family", "capacity_mwe", "Technology Mix – Pipeline", "technology_mix_pipeline.png",
    )
    _bar(
        taxonomy.sort_values("maturity_score", ascending=False),
        "reactor_type", "maturity_score", "Technology Maturity by Reactor Type", "maturity_by_technology.png",
    )

    # --- Distribution histograms ---
    _hist(reactors, "age_years", "Reactor Age Distribution (Operating Fleet)", "reactor_age_distribution.png")
    if "nuclear_share_percent" in countries.columns:
        _hist(countries, "nuclear_share_percent", "Nuclear Share Distribution by Country", "nuclear_share_by_country.png")
    if "nuclear_generation_twh" in countries.columns:
        _hist(countries, "nuclear_generation_twh", "Nuclear Generation Distribution by Country", "nuclear_generation_distribution.png")

    # --- Scenario charts ---
    _bar(
        scenarios[scenarios.year == 2050].groupby("scenario", as_index=False)["capacity_gwe"].sum(),
        "scenario", "capacity_gwe", "2050 Capacity Scenarios", "capacity_scenarios_2050.png",
    )
    _bar(
        scenarios.groupby("scenario", as_index=False)["estimated_generation_twh"].sum(),
        "scenario", "estimated_generation_twh", "Estimated Generation by Scenario", "estimated_generation_scenarios.png",
    )

    # --- Country strategy ---
    _bar(
        countries.sort_values("policy_signal_score", ascending=False),
        "country", "policy_signal_score", "Policy Signal Score by Country", "country_strategy_clusters.png",
    )
    _bar(
        countries.sort_values("policy_signal_score", ascending=False),
        "country", "policy_signal_score", "Policy Signal by Country", "policy_signal_by_country.png",
    )

    # --- Risk ---
    _bar(
        pipeline.groupby("country", as_index=False)["delay_risk_score"].mean().sort_values("delay_risk_score", ascending=False),
        "country", "delay_risk_score", "Average Delay Risk by Country", "risk_by_country.png",
    )

    # --- Region ---
    _bar(
        reactors.groupby("region", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False),
        "region", "capacity_mwe", "Capacity by Region", "capacity_by_region.png",
    )
    _bar(
        pipeline.groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False),
        "country", "capacity_mwe", "Pipeline Capacity by Country", "pipeline_by_region.png",
    )

    # --- Data quality heatmap ---
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.heatmap(reactors.isna(), cbar=False, ax=ax)
    ax.set_title("Data Quality – Missingness Heatmap")
    fig.savefig(config.FIGURES / "data_quality_heatmap.png")
    plt.close(fig)

    _bar(
        reactors.groupby("source_name", as_index=False).size(),
        "source_name", "size", "Source Coverage", "source_coverage_map.png",
    )

    # --- NLP charts ---
    kw_path = config.ANALYTICS / "nlp_keywords.csv"
    if kw_path.exists():
        kw = (
            pd.read_csv(kw_path)
            .groupby("term", as_index=False)["count"]
            .sum()
            .sort_values("count", ascending=False)
        )
        _bar(kw, "term", "count", "Top Policy Keywords", "top_policy_keywords.png", top=20)

    topic_heat = topics.pivot_table(
        index="country", columns="topic", values="present", aggfunc="max", fill_value=0
    )
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.heatmap(topic_heat, annot=True, cmap="Blues", ax=ax)
    ax.set_title("Technology Topic Heatmap by Country")
    fig.savefig(config.FIGURES / "technology_topic_heatmap.png")
    plt.close(fig)

    # --- EDA report ---
    report = f"""# Full EDA Report

## Executive Readout
EDA generated from processed reactor, country, pipeline, scenario and NLP tables.
Sample data is clearly labeled; official/manual exports can be added through the documented adapters.

## Data Quality
- Reactor rows: {len(reactors)}
- Countries represented: {reactors['country'].nunique()}
- Duplicate reactor IDs after cleaning: {int(reactors.duplicated('reactor_id').sum())}
- Main limitation: sample data demonstrates workflow; not source-of-record.

## Global Fleet
Operating capacity concentrates in countries with mature nuclear programs. The sample
highlights the gap between operating, under-construction, and planned/proposed capacity.

## Reactor Pipeline
Construction-stage projects get higher realization scores. Large first-of-a-kind projects
and early advanced technologies get higher delay-risk scores.

## Technology Mix
Commercial LWR families dominate maturity scoring. SMR, fast reactor, molten salt and
thorium concepts are treated as strategic signals and scenario inputs, not near-term forecasts.

## Scenario Findings
The scenario engine translates capacity into TWh using capacity factor assumptions and project
realization adjustments. This is a strategic planning tool, not an official forecast.

## NLP Signals
Policy text tagging detects SMR, Gen IV, financing, licensing/delay, energy security and
decarbonization signals by country.
"""
    eda_dir = config.OUTPUTS / "eda"
    eda_dir.mkdir(parents=True, exist_ok=True)
    (eda_dir / "full_eda_report.md").write_text(report, encoding="utf-8")
