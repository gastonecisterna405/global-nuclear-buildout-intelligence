from __future__ import annotations
import sqlite3
import pandas as pd
from src import config

QUERIES = {
    "top_countries_by_operating_capacity": "select country, sum(capacity_mwe) capacity_mwe from reactors where status_group='Operating' group by country order by capacity_mwe desc;",
    "top_countries_by_construction_capacity": "select country, sum(capacity_mwe) capacity_mwe from reactors where status_group='Construction' group by country order by capacity_mwe desc;",
    "pipeline_by_technology": "select technology_family, count(*) projects, sum(capacity_mwe) capacity_mwe from pipeline_projects group by technology_family order by capacity_mwe desc;",
    "pipeline_by_region": "select c.region, count(*) projects, sum(p.capacity_mwe) capacity_mwe from pipeline_projects p left join countries c using(country) group by c.region;",
    "smr_projects_by_status": "select status_group, count(*) projects, sum(capacity_mwe) capacity_mwe from pipeline_projects where technology_family like '%Small Modular%' group by status_group;",
    "geniv_concepts_by_maturity_score": "select reactor_type, technology_family, maturity_score from technologies where geniv_flag=1 order by maturity_score desc;",
    "estimated_2050_twh_by_scenario": "select scenario, sum(estimated_generation_twh) twh from capacity_scenarios where year=2050 group by scenario;",
    "high_share_aging_fleets": "select country, nuclear_share_percent, average_fleet_age from countries where nuclear_share_percent >= 20 order by average_fleet_age desc;",
    "new_entrant_planned_projects": "select country, planned_reactor_count, planned_capacity_mwe from countries where operating_reactor_count=0 and planned_reactor_count>0;",
    "high_risk_projects_by_country": "select country, reactor_name, delay_risk_score from project_risk_scores where risk_level='High' order by delay_risk_score desc;",
    "project_risk_by_technology": "select technology_family, avg(delay_risk_score) avg_delay_risk from project_risk_scores group by technology_family;",
    "data_quality_by_source": "select source_name, avg(source_confidence) avg_confidence, count(*) rows from reactors group by source_name;",
    "policy_keyword_counts_by_country": "select country, topic, sum(present) count from nlp_topics group by country, topic;",
    "average_construction_duration_by_reactor_type": "select reactor_type_standardized, avg(cast(strftime('%Y', grid_connection_date) as integer)-cast(strftime('%Y', construction_start_date) as integer)) avg_years from reactors where construction_start_date is not null and grid_connection_date is not null group by reactor_type_standardized;",
    "capacity_added_by_decade": "select (cast(strftime('%Y', commercial_operation_date) as integer)/10)*10 decade, sum(capacity_mwe) capacity_mwe from reactors where commercial_operation_date is not null group by decade;",
}

def run_sql_queries() -> None:
    db = config.OUTPUTS / "nuclear_buildout.sqlite"
    with sqlite3.connect(db) as conn:
        for name, query in QUERIES.items():
            try:
                pd.read_sql_query(query, conn).to_csv(config.SQL_OUT / f"{name}.csv", index=False)
            except Exception as exc:
                (config.SQL_OUT / f"{name}.error.txt").write_text(str(exc), encoding="utf-8")
