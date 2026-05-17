# Decisions Required and Defaults Taken

## Dashboard
Decision: Build both Streamlit and Power BI outputs.
Default taken: Streamlit dashboard plus Power BI-ready CSV exports and guide.

## Data Sources
Decision: Prioritize public/open sources and manual workflows where official bulk access is unreliable.
Default taken: Build adapters/templates for IAEA PRIS, RDS-1, ARIS, SMR catalogue, WNA, GEM, EIA; optional download adapters for OWID and World Bank.

## Dirty Raw Data
Decision: Include dirty/raw sample data and process it through the pipeline.
Default taken: `data/raw/sample/dirty_*` is generated and explicitly labeled sample-only.

## SMR / Gen IV / Thorium Treatment
Decision: Whether to forecast these as targets or treat them as maturity/scenario indicators.
Default taken: maturity and scenario indicators. Reason: deployment history is too thin for honest deterministic forecasting.

## Geography
Decision: Global coverage.
Default taken: global schema with sample spotlight countries. No paid APIs are required. Google Cloud Platform could host a production version but is not needed locally.

## Modeling
Decision: Include several models and scores.
Default taken: XGBoost/fallback regressor, Statsmodels trend, Logistic Regression, Random Forest, XGBoost classifier when installed, Random Forest maturity model, KMeans/PCA clustering, transparent heuristic scores.

## Optional Modules
Decision: Include electricity value proxy; defer uranium/hydrogen/desalination/data centers.
Default taken: value proxy implemented; other modules documented as future extensions.

## Priority
Decision: Completeness vs aesthetics.
Default taken: end-to-end completeness first, then professional dashboard polish.
