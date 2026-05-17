# Methodology

The pipeline standardizes reactor status, reactor types, technology families, country context, pipeline maturity and technology maturity. Capacity scenarios convert GWe into TWh using capacity factor assumptions.

Project risk scoring combines project stage, technology maturity, country experience, GDP context and size complexity. Realization probability is a decision-support score, not an official probability.

Forecasting uses a scenario-derived target in the portfolio build. In production, the same model structure should be trained on historical project snapshots and actual completion outcomes.

NLP uses NLTK-compatible tokenization/stopwords, keyword extraction and rule-based topic tagging for nuclear policy and technology signals.
