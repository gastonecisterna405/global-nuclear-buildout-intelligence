from __future__ import annotations
from src import config

def generate_model_card() -> str:
    text = '''# Model Card

## Capacity Forecasting Model
- Target: scenario-derived expected 2035 capacity.
- Features: operating/construction/planned/proposed capacity, GDP, population, demand, nuclear share, fleet age, region, policy signal.
- Intended use: portfolio model demonstration and scenario support.
- Limitation: sample target is heuristic; production requires historical snapshots.

## Project Realization Classifiers
- Models: Logistic Regression, Random Forest, XGBoost when installed.
- Target: high realization label derived from transparent scoring.
- Intended use: decision-support ranking, not official prediction.

## Technology Maturity Model
- Target: maturity score from deployment and novelty factors.
- Intended use: compare technology readiness and explain scenario assumptions.

## Country Clustering
- Models: KMeans and PCA.
- Intended use: market segmentation and strategy discussion.
'''
    (config.DOCS / "model_card.md").write_text(text, encoding="utf-8")
    (config.REPORTS / "model_summary.md").write_text(text, encoding="utf-8")
    return text
