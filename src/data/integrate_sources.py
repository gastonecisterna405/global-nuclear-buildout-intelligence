from __future__ import annotations

from src import config
from src.data.clean_reactor_data import clean_reactors
from src.data.clean_country_data import clean_country_context
from src.features.reactor_features import add_reactor_feature_flags
from src.features.technology_features import build_technology_taxonomy
from src.features.pipeline_features import build_reactor_pipeline
from src.features.country_features import build_country_profiles
from src.features.scenario_features import build_capacity_scenarios


def integrate_all():
    reactors = add_reactor_feature_flags(clean_reactors())
    taxonomy = build_technology_taxonomy(reactors)
    context = clean_country_context()
    pipeline = build_reactor_pipeline(reactors, taxonomy, context)
    countries = build_country_profiles(reactors, context, pipeline)
    scenarios = build_capacity_scenarios(countries, pipeline)
    reactors.to_csv(config.PROCESSED / "reactors_master.csv", index=False)
    return reactors, countries, pipeline, taxonomy, scenarios
