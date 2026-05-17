# Global Nuclear Buildout Intelligence Platform

**End-to-end ML and analytics platform for nuclear capacity forecasting, technology maturity scoring, project risk assessment, and electricity supply scenarios.**

Built as a portfolio project by a Nuclear Engineer transitioning into data science. The platform demonstrates a production-style analytics pipeline — from raw, heterogeneous data to interactive dashboard and executive reporting.

---

## What it does

Governments, utilities, and investors need to understand where nuclear capacity could grow, which reactor technologies are gaining traction, and how realistic project pipelines are. Public data on this is fragmented across databases, PDFs, and industry publications.

This platform:
- **Ingests and standardizes** reactor, country, technology, and policy data from multiple public sources
- **Scores projects and technologies** using transparent, auditable heuristics (maturity, delay risk, realization probability)
- **Forecasts capacity** with XGBoost/Random Forest cross-sectional models and Holt-Winters time series
- **Clusters countries** by nuclear strategy using KMeans + PCA
- **Extracts policy signals** from text using NLP (keyword extraction, topic tagging)
- **Models electricity scenarios** under Conservative / Base / Accelerated buildout assumptions
- **Publishes results** through a 14-page Streamlit dashboard, Power BI-ready CSVs, SQLite database, and executive reports

---

## Architecture

```
Data Sources
├── IAEA PRIS / RDS-1 / ARIS / SMR Catalogue  (manual template workflow)
├── World Nuclear Association / Global Energy Monitor  (manual template)
├── Our World in Data Energy  (optional download)
└── World Bank WDI  (optional API)
        │
        ▼
  raw/  (dirty CSVs + manual exports)
        │
  clean_reactor_data.py ──► reactors_cleaned.csv  (interim/)
  clean_country_data.py ──► country_context.csv
        │
  integrate_sources.py
  ├── add_reactor_feature_flags()   — SMR/Gen IV/molten salt/thorium/fast flags
  ├── build_technology_taxonomy()   — 13 types, maturity scores
  ├── build_reactor_pipeline()      — maturity + delay risk + realization probability
  ├── build_country_profiles()      — operating/construction/planned capacity aggregates
  └── build_capacity_scenarios()    — Conservative / Base / Accelerated to 2050
        │
  processed/  (reactors_master.csv, reactor_pipeline.csv, country_nuclear_profile.csv, ...)
        │
  ┌─────┴──────┬──────────┬────────┬────────┐
  ML models   NLP       SQL     Reports  Dashboard
  XGBoost     NLTK    SQLite   Markdown  Streamlit
  KMeans+PCA  topics  15 queries  PDF-ready  14 pages
  Statsmodels
        │
  outputs/  (predictions/, metrics/, figures/, reports/)
  data/powerbi/  (fact + dim tables)
```

---

## Quickstart

```bash
git clone https://github.com/<your-handle>/global-nuclear-buildout-intelligence
cd global-nuclear-buildout-intelligence

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python run_pipeline.py      # builds all processed tables, models, and reports
streamlit run src/dashboard/app.py
```

The pipeline runs end-to-end on **labeled sample data** so the full system works before any manual source files are added. See [Data Sources](#data-sources) for how to plug in real data.

---

## Results (sample data)

> All numbers below are from the labeled sample dataset (19 reactor records, 16 countries). They demonstrate the pipeline and scoring logic — not official statistics. Replace with IAEA PRIS exports for production use.

| Layer | Key output |
|---|---|
| **Fleet** | 7 operating units · 8.5 GWe operating · 6 units under construction · 6.3 GWe |
| **Pipeline** | 13 pipeline projects across Construction / Planned / Proposed stages |
| **Technology taxonomy** | 13 reactor types scored across 8 technology families |
| **Capacity forecast (XGBoost)** | R² = 0.67 on heuristic target (cross-sectional, 16 countries) |
| **Country clusters** | 3 clusters · silhouette = 0.19 |
| **2050 Base scenario** | ~6.2 GWe · ~47 TWh/yr (sample fleet only) |
| **Technology maturity** | Highest: VVER / PWR / BWR · Lowest: Thorium / Microreactor / MSR |
| **Policy NLP** | 6 countries tagged across 10 topic signals (SMR, Gen IV, financing, ...) |

---

## Notebooks

Run `python run_pipeline.py` first, then open any notebook from the `notebooks/` directory.

| Notebook | What it covers |
|---|---|
| [02 Data Cleaning](notebooks/02_data_cleaning_and_integration.ipynb) | Dirty → clean walkthrough, schema diff, data lineage |
| [03 Global Nuclear EDA](notebooks/03_global_nuclear_eda.ipynb) | Fleet capacity, tech mix, age distribution, GDP scatter, decade buildout |
| [04 Reactor Pipeline EDA](notebooks/04_reactor_pipeline_eda.ipynb) | Pipeline funnel, timeline, risk matrix, realization probability |
| [05 Technology Mix](notebooks/05_technology_mix_eda.ipynb) | SMR vs Gen IV vs commercial LWR, maturity scoring breakdown |
| [06 Forecasting](notebooks/06_forecasting_capacity_buildout.ipynb) | XGBoost feature importance, Holt-Winters trend, model limitations |
| [07 Project Risk Scoring](notebooks/07_project_risk_scoring.ipynb) | Classification pipeline, risk matrix, score sensitivity |
| [09 Country Clustering](notebooks/09_country_clustering.ipynb) | KMeans + PCA segmentation, cluster profiles |
| [10 NLP Policy Intelligence](notebooks/10_nlp_policy_and_technology_text.ipynb) | Keyword extraction, topic tagging, country signal heatmap |

---

## Dashboard pages

```
Executive Overview · Global Nuclear Map · Country Deep Dive · Reactor Pipeline ·
Technology Mix · SMR / Gen IV / Thorium Watch · Forecasting · Project Risk Scoring ·
Electricity Supply Scenarios · Country Strategy Clustering · NLP / Policy Intelligence ·
Data Quality & Source Coverage · Executive Report · Power BI Export
```

All sidebar filters (country, region, status, technology, scenario, capacity factor, price) propagate across pages.

---

## Data sources

| Source | Type | Ingestion |
|---|---|---|
| IAEA PRIS | Official reactor database | Manual template (`data/raw/iaea_pris/`) |
| IAEA RDS-1 | Capacity projections to 2050 | Manual template |
| IAEA ARIS / SMR Catalogue | Advanced reactor designs | Manual template |
| World Nuclear Association | Country profiles, pipeline | Manual template |
| Global Energy Monitor | Facility-level tracker | Manual template |
| Our World in Data Energy | Generation + nuclear share | Optional download |
| World Bank WDI | GDP, population | Optional API |
| Labeled sample data | Demo fallback | Auto-generated |

Manual templates are created automatically at `data/raw/*/` when you run the pipeline. Fill them with official exports to replace sample data.

---

## Tech stack

| Layer | Tools |
|---|---|
| Data | pandas · numpy · requests |
| ML | scikit-learn · XGBoost · statsmodels |
| NLP | NLTK |
| Visualization | matplotlib · seaborn · plotly |
| Dashboard | Streamlit |
| Storage | SQLite · CSV (Power BI) |
| Scale-out | PySpark / Databricks template (`spark/`) |
| Tests | pytest (24 tests) |

---

## Project structure

```
├── run_pipeline.py          # single entry point: runs all 21 pipeline steps
├── src/
│   ├── data/                # ingestion, cleaning, sample data, source registry
│   ├── features/            # reactor flags, taxonomy, pipeline scoring, scenarios
│   ├── models/              # XGBoost, Statsmodels, clustering, risk classifier, maturity
│   ├── eda/                 # EDA figure generation and report
│   ├── nlp/                 # text cleaning, keyword extraction, topic tagging
│   ├── sql/                 # SQLite build, 15 analytical queries, Power BI export
│   ├── reports/             # executive report, model card, interview brief
│   ├── dashboard/           # Streamlit app (app.py routes to 14 page modules)
│   └── utils/               # paths, constants, validation, plotting theme
├── notebooks/               # 11 portfolio-facing analysis notebooks
├── tests/                   # 24 pytest tests
├── data/
│   ├── raw/                 # source files + manual templates
│   ├── interim/             # cleaned pre-integration tables
│   └── processed/           # final analytical tables
├── outputs/
│   ├── figures/             # EDA charts (PNG)
│   ├── metrics/             # JSON model metrics
│   ├── predictions/         # forecast and risk CSVs
│   └── reports/             # markdown reports
├── models/                  # serialized joblib models
├── spark/                   # PySpark ETL + Databricks notebook template
└── docs/                    # model card, Power BI guide, interview brief
```

---

## Methodology notes

**Forecasting caveat:** The XGBoost model's target is a scenario-derived heuristic (not historical snapshots), so metrics measure fit to a formula rather than real-world predictive accuracy. A production model would require timestamped PRIS data to build a proper supervised dataset.

**Risk scoring:** Project maturity and delay risk are transparent, auditable heuristics (weighted combination of status, technology maturity, country experience, and GDP proxy). Labels are clearly derived from scoring rules — not from historical realization outcomes.

**Scenarios:** `TWh/yr = capacity_GW × capacity_factor × 8.76`. Capacity factor, realization adjustment, and price per MWh are user-configurable in the dashboard. Not a market forecast.

---

## Interview pitch

> I built a strategic nuclear analytics platform that uses public reactor, energy, and economic data to analyze global buildout, classify reactor technologies, forecast capacity, score project risk, estimate electricity supply scenarios, and communicate results through dashboards and executive reports. The architecture mirrors a real consulting data product: transparent scoring, auditable heuristics, honest uncertainty, and a full ingestion-to-output pipeline.

---

## License

MIT
