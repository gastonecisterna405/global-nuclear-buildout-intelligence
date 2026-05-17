# Global Nuclear Buildout Intelligence Platform

**Reactor Pipeline Forecasting, Technology Mix Scoring & Nuclear Electricity Supply Scenarios**

This is a professional machine learning and analytics project for strategic nuclear buildout intelligence. It combines reactor pipeline data architecture, public-source ingestion workflows, dirty raw sample processing, EDA, machine learning, technology maturity scoring, country clustering, NLP policy intelligence, SQL, Power BI exports, Streamlit dashboarding and executive reporting.

## Why It Matters
Governments, utilities, investors and consultants need to understand where nuclear power could grow, which reactor technologies are gaining traction, how realistic the project pipeline is and how much electricity nuclear could provide under different scenarios.

## Business Problem
Nuclear project data is fragmented across official databases, PDFs, industry pages and country policy documents. This platform turns that fragmented information into decision-ready analytics.

## Technical Problem
The project standardizes heterogeneous reactor, country, technology, scenario and text data into reusable analytical tables, then layers ML and reporting outputs on top.

## Data Sources
The source registry covers IAEA PRIS, IAEA RDS-1, IAEA ARIS, IAEA SMR publications, World Nuclear Association, Global Energy Monitor, Our World in Data, World Bank WDI and EIA. Some sources are manual-template workflows because reliable public bulk ingestion is not always available.

## Data Limitations
Sample data is clearly labeled and exists so the full system can run before manual source files are added. It must not be presented as official data.

## Architecture
Raw/manual sources -> cleaning -> processed tables -> features -> models/NLP/scenarios -> EDA/report/dashboard/SQL/Power BI.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py
```

## Run Dashboard
```bash
streamlit run src/dashboard/app.py
```

## Power BI
Run the pipeline and import CSV files from `data/powerbi/`. See `docs/powerbi_guide.md`.

## EDA Overview
EDA covers data quality, global fleet, pipeline, technology mix, country strategy, scenarios and NLP policy intelligence. Figures are saved in `outputs/figures/`.

## Modeling Approach
The project includes XGBoost/fallback capacity forecasting, Statsmodels trend forecasting, logistic/random forest/XGBoost project scoring, technology maturity scoring and KMeans/PCA country clustering.

## Forecasting Methodology
Forecasting is scenario-informed and honest about uncertainty. Production validation would require historical snapshots.

## Scoring Methodology
Project realization and delay risk are transparent decision-support scores when true labels are not available.

## Technology Maturity
Maturity scoring combines commercial deployment, operating/under-construction units, design maturity, novelty, regulatory familiarity and source confidence.

## Electricity Scenarios
`TWh/year = capacity_GW * capacity_factor * 8.76`. Price per MWh is a configurable value proxy, not an electricity market model.

## NLP
NLTK-compatible cleaning, tokenization, keyword extraction and topic tagging identify SMR, Gen IV, financing, licensing, energy security and decarbonization signals.

## GenAI Reporting
The deterministic report generator summarizes structured outputs and does not invent facts. Optional API extension can be added later.

## PySpark / Databricks
`spark/pyspark_etl.py` and `spark/databricks_notebook_template.py` show how the architecture scales to Delta Lake and scheduled refresh.

## SQL Layer
The pipeline builds SQLite tables and exports query results to `outputs/tables/sql_query_results/`.

## Dashboard Pages
Executive Overview, Global Map, Country Deep Dive, Pipeline, Technology Mix, SMR/Gen IV Watch, Forecasting, Project Risk, Electricity Scenarios, Clustering, NLP, Data Quality, Executive Report and Power BI Export.

## Key Results
Run `python run_pipeline.py` to generate current sample-based results and reports.

## Future Improvements
Add official PRIS exports, recurring GEM/WNA snapshots, validated project outcome labels, uranium supply, hydrogen/desalination modules, data-center demand and cloud scheduled refresh.

## Interview Pitch
I built a strategic nuclear analytics platform that uses public reactor, energy and economic data to analyze global nuclear buildout, classify reactor technologies, forecast capacity growth, score project and technology maturity risks, estimate electricity supply scenarios and communicate results through dashboards and executive reports.
