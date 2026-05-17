from __future__ import annotations

import pandas as pd
from src import config

SOURCES = [
    {
        "source_name": "IAEA PRIS",
        "source_type": "official reactor database",
        "url": "https://pris.iaea.org/PRIS/",
        "fields_used": "reactor status, country, type, capacity, dates",
        "limitations": "Interactive/public pages are not always bulk-download friendly; manual export may be required.",
        "reliability_rating": "high",
        "ingestion_mode": "manual_template",
    },
    {
        "source_name": "IAEA RDS-1",
        "source_type": "official projection report",
        "url": "https://www.iaea.org/publications/search/type/reference-data-series",
        "fields_used": "low/high nuclear capacity projections to 2050",
        "limitations": "Often published as PDF tables; manual table extraction may be required.",
        "reliability_rating": "high",
        "ingestion_mode": "manual_template",
    },
    {
        "source_name": "IAEA ARIS",
        "source_type": "official advanced reactor information system",
        "url": "https://aris.iaea.org/",
        "fields_used": "advanced reactor design metadata",
        "limitations": "Design pages vary by completeness and may require manual review.",
        "reliability_rating": "high",
        "ingestion_mode": "manual_template",
    },
    {
        "source_name": "IAEA SMR Catalogue",
        "source_type": "official/publication catalogue",
        "url": "https://aris.iaea.org/Publications/SMR_booklet_2022.pdf",
        "fields_used": "SMR design metadata and use cases",
        "limitations": "PDF catalogue; manually curated table recommended.",
        "reliability_rating": "high",
        "ingestion_mode": "manual_template",
    },
    {
        "source_name": "World Nuclear Association",
        "source_type": "industry association",
        "url": "https://world-nuclear.org/information-library",
        "fields_used": "country profiles, planned/proposed reactors, technology descriptions",
        "limitations": "Useful strategic source; status definitions may differ from official datasets.",
        "reliability_rating": "medium-high",
        "ingestion_mode": "manual_template",
    },
    {
        "source_name": "Global Energy Monitor Nuclear Power Tracker",
        "source_type": "NGO facility tracker",
        "url": "https://globalenergymonitor.org/projects/global-nuclear-power-tracker/",
        "fields_used": "facility/unit status, capacity, owner/operator, coordinates",
        "limitations": "Excellent facility view; cross-source reconciliation required.",
        "reliability_rating": "medium-high",
        "ingestion_mode": "manual_template",
    },
    {
        "source_name": "Our World in Data Energy",
        "source_type": "open data",
        "url": "https://github.com/owid/energy-data",
        "fields_used": "generation by source, electricity demand, nuclear share",
        "limitations": "Country/year energy indicators; not a reactor project source.",
        "reliability_rating": "high",
        "ingestion_mode": "download_optional",
    },
    {
        "source_name": "World Bank WDI",
        "source_type": "open API",
        "url": "https://api.worldbank.org/v2/",
        "fields_used": "GDP, population, income group context",
        "limitations": "Coverage and latest-year availability vary by indicator.",
        "reliability_rating": "high",
        "ingestion_mode": "download_optional",
    },
    {
        "source_name": "EIA International",
        "source_type": "government energy data",
        "url": "https://www.eia.gov/international/data/world",
        "fields_used": "energy context where available",
        "limitations": "API access may require key depending on endpoint.",
        "reliability_rating": "high",
        "ingestion_mode": "documented_optional",
    },
    {
        "source_name": "Labeled Dirty Sample Data",
        "source_type": "sample fallback",
        "url": "local:data/raw/sample",
        "fields_used": "complete demo schema for pipeline execution",
        "limitations": "Sample data for demonstration only; never presented as real source-of-record.",
        "reliability_rating": "sample-only",
        "ingestion_mode": "generated",
    },
]

def register_sources() -> pd.DataFrame:
    df = pd.DataFrame(SOURCES)
    df["date_accessed"] = "2026-05-17"
    out = config.PROCESSED / "data_sources.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return df
