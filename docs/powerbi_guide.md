# Power BI Guide

1. Open Power BI Desktop.
2. Import CSV files from `data/powerbi/`.
3. Use `dim_country`, `dim_region`, `dim_technology` and `dim_date` as dimensions.
4. Connect fact tables on country, region, technology and year fields where available.
5. Suggested DAX measures:
   - Total Operating Capacity MW = SUM(fact_reactors[capacity_mwe])
   - Total Construction Capacity MW = CALCULATE(SUM(fact_reactors[capacity_mwe]), fact_reactors[status_group] = "Construction")
   - Total Planned Capacity MW = CALCULATE(SUM(fact_reactors[capacity_mwe]), fact_reactors[status_group] = "Planned")
   - Estimated Nuclear Generation TWh = SUM(fact_capacity_scenarios[estimated_generation_twh])
   - High Risk Projects = CALCULATE(COUNTROWS(fact_project_risk_scores), fact_project_risk_scores[risk_level] = "High")
   - Average Maturity Score = AVERAGE(fact_technology_maturity[maturity_score])
   - Average Realization Probability = AVERAGE(fact_project_risk_scores[realization_probability])
   - Nuclear Share % = AVERAGE(dim_country[nuclear_share_percent])
   - Estimated Market Value = SUM(fact_capacity_scenarios[estimated_generation_twh]) * 1000000 * 75
   - Countries With Active Pipeline = DISTINCTCOUNT(fact_reactor_pipeline[country])
6. Suggested pages: Executive Overview, Pipeline, Technology Mix, Risk, Scenarios, Country Deep Dive, Data Quality.
7. Publish to Power BI Service after building the report.
8. Local refresh reads CSV files; cloud refresh requires files in OneDrive/SharePoint/cloud storage or a gateway.
9. Limitations: sample data is not source-of-record and manual sources require refresh discipline.
10. Add screenshots of the Power BI pages to the README after report creation.
