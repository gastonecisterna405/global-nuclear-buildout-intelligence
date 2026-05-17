from __future__ import annotations
from src import config

def generate_interview_brief() -> str:
    text = '''# Interview Project Brief

## One-Sentence Explanation
I built a strategic nuclear analytics platform that uses public reactor, energy and economic data structures to analyze global nuclear buildout, classify technologies, forecast capacity, score risks, model electricity scenarios and communicate insights through Streamlit, Power BI exports, SQL and executive reporting.

## 30-Second Pitch
This project translates fragmented nuclear buildout information into a consulting-style analytics product. It integrates reactor pipeline data, country context, technology maturity, policy-text signals and scenario modelling to answer where nuclear could grow, how realistic projects are and how much electricity different buildout cases could provide.

## 2-Minute Pitch
The platform is designed for energy consultants, utilities, investors and policy teams. It separates real data ingestion from manual-source workflows, creates standardized reactor and country tables, runs EDA, trains several ML models, scores technology and project risk, clusters countries by nuclear strategy, estimates TWh and value scenarios, and publishes results through Streamlit and Power BI-ready tables. It is honest about uncertainty: SMRs and Gen IV are treated as maturity and scenario signals unless deployment data supports forecasting.

## Technical Architecture
Raw/manual adapters -> cleaning -> integrated processed tables -> feature engineering -> ML/scenario/NLP -> SQLite/Power BI/report/dashboard outputs.

## Business Value
Market screening, technology strategy, infrastructure diligence, policy intelligence and executive communication.

## Connection to Nuclear Background
The reactor taxonomy, maturity scoring, capacity-factor scenario logic and careful treatment of advanced reactors reflect nuclear engineering judgment.

## Job Requirement Mapping
- Python/Pandas/NumPy: pipeline and analytics tables.
- Scikit-learn/XGBoost/Statsmodels/SciPy awareness: forecasting, classification, clustering and scenario modeling.
- NLTK: policy text cleaning, keyword extraction and topic tagging.
- SQL: SQLite database and query exports.
- Visualization/dashboard: EDA figures and Streamlit.
- Reporting/GenAI: deterministic structured report generator with optional API extension.
- PySpark/Databricks: Spark ETL template and production architecture.
- Stakeholder communication: README, report, Power BI guide and interview brief.

## Strong Interview Answers
- Forecasts are scenarios informed by data, not certainty.
- SMR/Gen IV outputs are maturity and strategic signals.
- Public data limitations are handled with source inventory, manual schemas and sample-only fallbacks.
- The architecture can scale with Databricks, Delta Lake, scheduled ingestion and model registry.

## Questions to Practice
Why this project? What is the business value? How reliable are the forecasts? How do you avoid overclaiming? What is the difference between forecasting and scenario modelling? How does Generative AI add value? How would this scale in a real company?

## Weak Answers to Avoid
Avoid saying the project predicts the future, proves SMRs will deploy at scale, or uses sample data as official evidence.

## Final Summary to Memorize
I built an end-to-end nuclear buildout intelligence platform that combines reactor data architecture, ML, scenario modeling, NLP, SQL, dashboards and executive reporting into a transparent consulting deliverable.
'''
    (config.DOCS / "interview_project_brief.md").write_text(text, encoding="utf-8")
    return text
