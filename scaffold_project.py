"""One-time scaffold helper for the Global Nuclear Buildout project.

This utility creates the repository assets requested for the portfolio project.
It is intentionally kept in the repo so the generated structure is auditable.
"""

from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent


DIRS = [
    "data/raw/iaea_pris",
    "data/raw/iaea_rds1",
    "data/raw/iaea_aris",
    "data/raw/iaea_smr",
    "data/raw/world_nuclear_association",
    "data/raw/global_energy_monitor",
    "data/raw/our_world_in_data",
    "data/raw/world_bank",
    "data/raw/eia",
    "data/raw/sample",
    "data/interim",
    "data/processed",
    "data/analytics",
    "data/powerbi",
    "notebooks",
    "src/data",
    "src/features",
    "src/eda",
    "src/models",
    "src/nlp",
    "src/sql",
    "src/reports",
    "src/dashboard/pages",
    "src/dashboard/components",
    "src/dashboard/assets",
    "src/utils",
    "sql",
    "spark",
    "models",
    "outputs/figures",
    "outputs/eda",
    "outputs/metrics",
    "outputs/predictions",
    "outputs/reports",
    "outputs/tables/sql_query_results",
    "outputs/dashboard_screenshots",
    "docs",
    "tests",
    "powerbi/exported_tables",
]


NOTEBOOKS = [
    "01_data_source_audit.ipynb",
    "02_data_cleaning_and_integration.ipynb",
    "03_global_nuclear_eda.ipynb",
    "04_reactor_pipeline_eda.ipynb",
    "05_technology_mix_eda.ipynb",
    "06_forecasting_capacity_buildout.ipynb",
    "07_project_risk_scoring.ipynb",
    "08_technology_maturity_scoring.ipynb",
    "09_country_clustering.ipynb",
    "10_nlp_policy_and_technology_text.ipynb",
    "11_dashboard_prototyping.ipynb",
]


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    cleaned = text.lstrip("\n").rstrip()
    # Multi-line generated source strings live inside main(), so remove one
    # scaffold indent when the text itself starts indented. Inline strings are
    # left untouched so normal Python block indentation is preserved.
    lines = cleaned.splitlines()
    first = next((line for line in lines if line.strip()), "")
    if first.startswith("    "):
        indent = len(first) - len(first.lstrip(" "))
        prefix = " " * indent
        cleaned = "\n".join(line[indent:] if line.startswith(prefix) else line for line in lines)
    target.write_text(cleaned + "\n", encoding="utf-8")


def write_json(path: str, obj: object) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def notebook(title: str) -> dict:
    return {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n",
                    "\n",
                    "This notebook is a portfolio-facing analysis companion. The production pipeline lives in `run_pipeline.py` and `src/`.\n",
                    "\n",
                    "Run the pipeline first, then use this notebook for narrative exploration and interview walkthroughs.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "from pathlib import Path\n",
                    "import pandas as pd\n",
                    "ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n",
                    "processed = ROOT / 'data' / 'processed'\n",
                    "print(sorted(p.name for p in processed.glob('*.csv')))\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    for d in DIRS:
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    for package in [
        "src",
        "src/data",
        "src/features",
        "src/eda",
        "src/models",
        "src/nlp",
        "src/sql",
        "src/reports",
        "src/dashboard",
        "src/dashboard/pages",
        "src/dashboard/components",
        "src/utils",
    ]:
        write(f"{package}/__init__.py", "")
    for nb in NOTEBOOKS:
        write_json(f"notebooks/{nb}", notebook(nb.replace("_", " ").replace(".ipynb", "").title()))

    write("requirements.txt", """
    pandas>=2.0
    numpy>=1.24
    scikit-learn>=1.3
    xgboost>=2.0
    statsmodels>=0.14
    scipy>=1.10
    nltk>=3.8
    matplotlib>=3.7
    seaborn>=0.12
    plotly>=5.18
    streamlit>=1.33
    joblib>=1.3
    requests>=2.31
    pycountry>=23.12
    pytest>=7.0
    """)
    write("pyproject.toml", """
    [project]
    name = "global-nuclear-buildout-intelligence"
    version = "0.1.0"
    description = "Reactor pipeline forecasting, technology mix scoring, and nuclear electricity supply scenarios"
    requires-python = ">=3.10"

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    pythonpath = ["."]
    """)
    write(".gitignore", """
    __pycache__/
    .pytest_cache/
    .venv/
    .DS_Store
    *.db
    *.sqlite
    data/raw/manual_uploads/
    """)
    write(".streamlit/config.toml", """
    [theme]
    base = "light"
    primaryColor = "#2563eb"
    backgroundColor = "#f5f7fb"
    secondaryBackgroundColor = "#ffffff"
    textColor = "#17202a"
    font = "sans serif"

    [browser]
    gatherUsageStats = false
    """)

    write("src/config.py", """
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    DATA = ROOT / "data"
    RAW = DATA / "raw"
    INTERIM = DATA / "interim"
    PROCESSED = DATA / "processed"
    ANALYTICS = DATA / "analytics"
    POWERBI = DATA / "powerbi"
    OUTPUTS = ROOT / "outputs"
    FIGURES = OUTPUTS / "figures"
    METRICS = OUTPUTS / "metrics"
    PREDICTIONS = OUTPUTS / "predictions"
    REPORTS = OUTPUTS / "reports"
    MODELS = ROOT / "models"
    DOCS = ROOT / "docs"
    SQL_OUT = OUTPUTS / "tables" / "sql_query_results"
    CURRENT_YEAR = 2026
    """)

    write("src/utils/paths.py", """
    from pathlib import Path
    from src import config

    REQUIRED_DIRS = [
        config.RAW, config.INTERIM, config.PROCESSED, config.ANALYTICS, config.POWERBI,
        config.FIGURES, config.METRICS, config.PREDICTIONS, config.REPORTS, config.MODELS,
        config.DOCS, config.SQL_OUT,
    ]

    def ensure_dirs() -> None:
        for path in REQUIRED_DIRS:
            Path(path).mkdir(parents=True, exist_ok=True)
    """)
    write("src/utils/logging.py", """
    import logging

    def get_logger(name: str) -> logging.Logger:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
        return logging.getLogger(name)
    """)
    write("src/utils/constants.py", """
    REGIONS = {
        "United States": "North America", "Canada": "North America", "Mexico": "North America",
        "Argentina": "Latin America", "Brazil": "Latin America",
        "France": "Europe", "United Kingdom": "Europe", "Poland": "Europe", "Turkey": "Europe",
        "Russia": "Eurasia", "China": "Asia", "India": "Asia", "Japan": "Asia",
        "South Korea": "Asia", "Bangladesh": "Asia", "UAE": "Middle East", "Egypt": "Africa",
    }
    STATUS_GROUPS = {
        "operating": "Operating", "in operation": "Operating", "under construction": "Construction",
        "construction": "Construction", "planned": "Planned", "proposed": "Proposed",
        "suspended": "Paused", "shutdown": "Shutdown", "retired": "Shutdown",
    }
    TECHNOLOGY_FAMILY = {
        "PWR": "Light Water Reactor", "VVER": "Light Water Reactor", "AP1000": "Light Water Reactor",
        "EPR": "Light Water Reactor", "BWR": "Light Water Reactor", "PHWR": "Heavy Water Reactor",
        "CANDU": "Heavy Water Reactor", "FBR": "Fast Reactor", "SFR": "Fast Reactor",
        "LFR": "Fast Reactor", "HTGR": "Gas-Cooled Reactor", "MSR": "Molten Salt Reactor",
        "SMR-LWR": "Small Modular Reactor", "Microreactor": "Microreactor",
    }
    """)
    write("src/utils/validation.py", """
    import pandas as pd

    def require_columns(df: pd.DataFrame, columns: list[str], name: str) -> None:
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise ValueError(f"{name} missing required columns: {missing}")
    """)
    write("src/utils/plotting.py", """
    import matplotlib.pyplot as plt
    import seaborn as sns

    def set_theme() -> None:
        sns.set_theme(style="whitegrid", palette="deep")
        plt.rcParams["figure.dpi"] = 140
        plt.rcParams["savefig.bbox"] = "tight"
    """)

    write("src/data/source_registry.py", """
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
    """)

    write("src/data/manual_ingestion_templates.py", """
    from __future__ import annotations

    import pandas as pd
    from src import config

    TEMPLATES = {
        "iaea_pris/pris_reactors_template.csv": [
            "reactor_name,country,status,reactor_type,net_capacity_mwe,construction_start_date,grid_connection_date,commercial_operation_date,shutdown_date,owner,operator,vendor,source_last_updated"
        ],
        "iaea_rds1/rds1_capacity_projection_template.csv": [
            "region,year,scenario,capacity_gwe,source_last_updated"
        ],
        "iaea_aris/aris_designs_template.csv": [
            "design_name,technology_family,reactor_type,coolant,moderator,fuel_type,neutron_spectrum,design_stage,smr_flag,geniv_flag,notes"
        ],
        "iaea_smr/smr_catalogue_template.csv": [
            "design_name,country,vendor,technology_family,capacity_mwe,coolant,moderator,use_cases,deployment_status,expected_timeline,notes"
        ],
        "world_nuclear_association/wna_pipeline_template.csv": [
            "reactor_name,country,status,reactor_type,capacity_mwe,expected_operation_year,owner,operator,vendor,notes"
        ],
        "global_energy_monitor/gem_nuclear_tracker_template.csv": [
            "plant_name,unit_name,country,status,capacity_mwe,latitude,longitude,owner,operator,construction_start_year,source_last_updated"
        ],
        "eia/eia_optional_template.csv": [
            "country,year,indicator,value,unit,source_last_updated"
        ],
    }

    def create_manual_templates() -> list[str]:
        written = []
        for rel, rows in TEMPLATES.items():
            path = config.RAW / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("\\n".join(rows) + "\\n", encoding="utf-8")
            written.append(str(path))
        return written
    """)

    write("src/data/ingest_owid_ember.py", """
    from __future__ import annotations

    import pandas as pd
    import requests
    from src import config

    OWID_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

    def ingest_owid(timeout: int = 20) -> pd.DataFrame:
        out = config.RAW / "our_world_in_data" / "owid_energy_data.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            r = requests.get(OWID_URL, timeout=timeout)
            r.raise_for_status()
            out.write_bytes(r.content)
            return pd.read_csv(out)
        except Exception as exc:
            marker = config.RAW / "our_world_in_data" / "DOWNLOAD_FAILED.txt"
            marker.write_text(f"OWID download failed; pipeline will use sample data. Reason: {exc}\\n", encoding="utf-8")
            return pd.DataFrame()
    """)
    write("src/data/ingest_world_bank.py", """
    from __future__ import annotations

    import pandas as pd
    import requests
    from src import config

    INDICATORS = {
        "NY.GDP.MKTP.CD": "gdp_current_usd",
        "SP.POP.TOTL": "population",
        "NY.GDP.PCAP.CD": "gdp_per_capita",
    }

    def ingest_world_bank(countries: list[str] | None = None, timeout: int = 20) -> pd.DataFrame:
        countries = countries or ["US", "CN", "RU", "IN", "FR", "GB", "KR", "JP", "CA", "AE", "TR", "EG", "PL", "BD", "AR", "BR"]
        frames = []
        for code in countries:
            for indicator, name in INDICATORS.items():
                url = f"https://api.worldbank.org/v2/country/{code}/indicator/{indicator}?format=json&per_page=70"
                try:
                    data = requests.get(url, timeout=timeout).json()
                    rows = data[1] if isinstance(data, list) and len(data) > 1 else []
                    for row in rows:
                        if row.get("value") is not None:
                            frames.append({"iso2": code, "country": row["country"]["value"], "year": int(row["date"]), "indicator": name, "value": row["value"]})
                except Exception:
                    continue
        df = pd.DataFrame(frames)
        out = config.RAW / "world_bank" / "world_bank_wdi_long.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        if not df.empty:
            df.to_csv(out, index=False)
        else:
            (config.RAW / "world_bank" / "DOWNLOAD_FAILED.txt").write_text("World Bank download failed; pipeline will use sample data.\\n", encoding="utf-8")
        return df
    """)

    for name, fn in {
        "ingest_iaea_pris.py": "IAEA PRIS",
        "ingest_iaea_rds1.py": "IAEA RDS-1",
        "ingest_iaea_aris.py": "IAEA ARIS",
        "ingest_iaea_smr.py": "IAEA SMR Catalogue",
        "ingest_wna.py": "World Nuclear Association",
        "ingest_gem.py": "Global Energy Monitor",
        "ingest_eia.py": "EIA International",
    }.items():
        write(f"src/data/{name}", f'''
        from __future__ import annotations
        import pandas as pd
        from src import config

        def ingest() -> pd.DataFrame:
            """Adapter skeleton for {fn}.

            This source is documented for manual ingestion because reliable bulk
            programmatic access may require interactive exports, PDFs, or API keys.
            See docs/data_sources_inventory.md and data/raw templates.
            """
            marker = config.RAW / "{name.replace('ingest_', '').replace('.py', '')}" / "MANUAL_INGESTION_REQUIRED.txt"
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text("{fn} requires manual/public export review for this portfolio build.\\n", encoding="utf-8")
            return pd.DataFrame()
        ''')

    write("src/data/sample_data.py", r'''
    from __future__ import annotations

    import pandas as pd
    from src import config

    RAW_REACTORS = [
        ["  Barakah-1 ", "Barakah", "Unit 1", "UAE", "operating", "PWR", "APR1400", 1345, 1345, "2012-07-18", "2020-08-19", "2021-04-06", "", 23.968, 52.227, "ENEC", "Nawah", "KEPCO", "GEM sample/WNA sample"],
        ["Barakah-4", "Barakah", "Unit 4", "UAE", "under construction", "PWR", "APR1400", 1345, 1345, "2015-09-02", "", "", "", 23.968, 52.227, "ENEC", "Nawah", "KEPCO", "GEM sample/WNA sample"],
        ["Vogtle-4", "Vogtle", "Unit 4", "United States", "operating", "PWR", "AP1000", 1117, 1250, "2013-11-19", "2024-03-01", "2024-04-29", "", 33.143, -81.762, "Georgia Power", "Southern Nuclear", "Westinghouse", "Sample"],
        ["Hinkley Point C-1", "Hinkley Point C", "Unit 1", "United Kingdom", "Construction", "PWR", "EPR", 1630, 1720, "2018-12-11", "", "", "", 51.205, -3.143, "EDF/CGN", "EDF", "Framatome", "Sample"],
        ["Akkuyu-1", "Akkuyu", "Unit 1", "Turkey", "Under Construction", "VVER", "VVER-1200", 1114, 1200, "2018-04-03", "", "", "", 36.144, 33.541, "Akkuyu Nuclear", "Rosatom", "Rosatom", "Sample"],
        ["El Dabaa-1", "El Dabaa", "Unit 1", "Egypt", "under construction", "VVER", "VVER-1200", 1114, 1200, "2022-07-20", "", "", "", 31.041, 28.497, "NPPA", "Rosatom", "Rosatom", "Sample"],
        ["Rooppur-1", "Rooppur", "Unit 1", "Bangladesh", "under construction", "VVER", "VVER-1200", 1114, 1200, "2017-11-30", "", "", "", 24.065, 89.047, "BAEC", "Rosatom", "Rosatom", "Sample"],
        ["Flamanville-3", "Flamanville", "Unit 3", "France", "operating", "PWR", "EPR", 1630, 1650, "2007-12-03", "2024-12-21", "2025-01-01", "", 49.536, -1.882, "EDF", "EDF", "Framatome", "Sample"],
        ["Taishan-1", "Taishan", "Unit 1", "China", "Operating", "PWR", "EPR", 1660, 1750, "2009-10-28", "2018-06-29", "2018-12-13", "", 21.918, 112.981, "TNPJVC", "CGN", "Framatome", "Sample"],
        ["Sanmen-1", "Sanmen", "Unit 1", "China", "operating", "PWR", "AP1000", 1157, 1250, "2009-04-19", "2018-06-30", "2018-09-21", "", 29.101, 121.641, "CNNC", "CNNC", "Westinghouse", "Sample"],
        ["Kudankulam-3", "Kudankulam", "Unit 3", "India", "planned", "VVER", "VVER-1000", 917, 1000, "", "", "", "", 8.169, 77.713, "NPCIL", "NPCIL", "Rosatom", "Sample"],
        ["Darlington SMR-1", "Darlington", "BWRX-300", "Canada", "planned", "SMR-LWR", "BWRX-300", 300, 300, "", "", "", "", 43.872, -78.719, "OPG", "OPG", "GE Hitachi", "Sample"],
        ["Natrium Demo", "Kemmerer", "Unit 1", "United States", "proposed", "SFR", "Natrium", 345, 345, "", "", "", "", 41.792, -110.538, "TerraPower", "TerraPower", "TerraPower/GEH", "Sample"],
        ["BN-800", "Beloyarsk", "Unit 4", "Russia", "operating", "FBR", "SFR", 789, 880, "2006-07-18", "2015-12-10", "2016-10-31", "", 56.842, 61.322, "Rosenergoatom", "Rosenergoatom", "OKBM", "Sample"],
        ["CAREM", "Atucha", "CAREM-25", "Argentina", "under construction", "SMR-LWR", "CAREM", 32, 32, "2014-02-08", "", "", "", -33.967, -59.205, "CNEA", "CNEA", "CNEA", "Sample"],
        ["Angra-3", "Angra", "Unit 3", "Brazil", "planned", "PWR", "PWR", 1245, 1405, "2010-06-01", "", "", "", -23.008, -44.458, "Eletronuclear", "Eletronuclear", "Siemens/Areva", "Sample"],
        ["Kori-2", "Kori", "Unit 2", "South Korea", "shutdown", "PWR", "PWR", 640, 650, "1977-12-23", "1983-04-09", "1983-07-25", "2023-04-08", 35.321, 129.294, "KHNP", "KHNP", "Westinghouse", "Sample"],
        ["Onagawa-2", "Onagawa", "Unit 2", "Japan", "operating", "BWR", "BWR", 796, 825, "1989-08-03", "1994-12-23", "1995-07-28", "", 38.402, 141.500, "Tohoku", "Tohoku", "Toshiba", "Sample"],
        ["Lubiatowo-Kopalino-1", "Lubiatowo-Kopalino", "Unit 1", "Poland", "planned", "PWR", "AP1000", 1117, 1250, "", "", "", "", 54.783, 17.850, "PEJ", "PEJ", "Westinghouse", "Sample"],
    ]

    COUNTRIES = [
        ["United States", "North America", "High income", 27360935000000, 81695, 334900000, 4300, 0.18, 19, 96],
        ["China", "Asia", "Upper middle income", 17794782000000, 12614, 1410000000, 9450, 0.05, 15, 65],
        ["Russia", "Eurasia", "Upper middle income", 2021420000000, 13817, 143800000, 1170, 0.20, 38, 29],
        ["India", "Asia", "Lower middle income", 3549919000000, 2485, 1428000000, 1900, 0.03, 25, 9],
        ["France", "Europe", "High income", 3030904000000, 44460, 68100000, 485, 0.65, 56, 61],
        ["United Kingdom", "Europe", "High income", 3340032000000, 48913, 68300000, 315, 0.14, 68, 6],
        ["Canada", "North America", "High income", 2140086000000, 53372, 40000000, 660, 0.15, 60, 14],
        ["UAE", "Middle East", "High income", 504173000000, 51426, 9800000, 160, 0.25, 4, 5],
        ["Turkey", "Europe", "Upper middle income", 1108022000000, 12985, 85300000, 335, 0.00, 0, 0],
        ["Egypt", "Africa", "Lower middle income", 395926000000, 3698, 110000000, 210, 0.00, 0, 0],
        ["Bangladesh", "Asia", "Lower middle income", 437415000000, 2688, 171000000, 95, 0.00, 0, 0],
        ["Argentina", "Latin America", "Upper middle income", 646075000000, 13935, 46200000, 145, 0.07, 50, 2],
        ["Brazil", "Latin America", "Upper middle income", 2173666000000, 10109, 216000000, 690, 0.02, 42, 2],
        ["Poland", "Europe", "High income", 811229000000, 22112, 36800000, 175, 0.00, 0, 0],
        ["Japan", "Asia", "High income", 4212945000000, 33834, 124500000, 980, 0.08, 54, 10],
        ["South Korea", "Asia", "High income", 1712793000000, 33147, 51700000, 590, 0.30, 46, 26],
    ]

    POLICY_DOCS = [
        ["policy-us-001", "United States", "DOE public strategy sample", "strategy", "Advanced nuclear fuel and demonstration policy", "2024-01-01", "Advanced reactors, SMR demonstrations, HALEU fuel supply, licensing modernization, clean firm power and industrial heat are recurring policy priorities."],
        ["policy-cn-001", "China", "public planning sample", "strategy", "Nuclear expansion and high temperature reactors", "2024-01-01", "Large PWR buildout continues with high temperature gas reactor demonstration, fast reactor activity and energy security framing."],
        ["policy-ca-001", "Canada", "provincial utility sample", "project", "Darlington SMR deployment", "2024-01-01", "SMR deployment, BWRX-300 licensing, grid reliability and clean electricity targets are emphasized."],
        ["policy-pl-001", "Poland", "government energy policy sample", "strategy", "First nuclear power program", "2024-01-01", "Energy security, coal replacement, financing, AP1000 technology selection and supply chain development are central."],
        ["policy-ar-001", "Argentina", "CNEA sample", "technology", "CAREM small reactor development", "2024-01-01", "CAREM small modular reactor development, domestic engineering capability and long nuclear experience are highlighted."],
        ["policy-ru-001", "Russia", "technology profile sample", "technology", "Fast reactor and closed fuel cycle development", "2024-01-01", "Fast reactor deployment, sodium-cooled technology, MOX fuel and closed fuel cycle strategy are emphasized."],
    ]

    def create_dirty_sample_data() -> None:
        sample = config.RAW / "sample"
        sample.mkdir(parents=True, exist_ok=True)
        reactors = pd.DataFrame(RAW_REACTORS, columns=[
            "reactor_name", "plant_name", "unit_name", "country", "status", "reactor_type",
            "design_name", "net_capacity_mwe", "gross_capacity_mwe", "construction_start_date",
            "grid_connection_date", "commercial_operation_date", "shutdown_date", "latitude",
            "longitude", "owner", "operator", "vendor", "source_name"
        ])
        reactors.loc[len(reactors)] = reactors.loc[1]
        reactors["net_capacity_mwe"] = reactors["net_capacity_mwe"].astype(object)
        reactors.loc[len(reactors) - 1, "net_capacity_mwe"] = "1,345"
        reactors.loc[4, "status"] = "Under-Construction "
        reactors.loc[10, "net_capacity_mwe"] = None
        reactors.to_csv(sample / "dirty_reactors_raw.csv", index=False)

        countries = pd.DataFrame(COUNTRIES, columns=[
            "country", "region", "income_group", "gdp_current_usd", "gdp_per_capita",
            "population", "electricity_generation_twh", "nuclear_share_fraction",
            "nuclear_experience_years", "historical_completed_reactors"
        ])
        countries.to_csv(sample / "dirty_country_context_raw.csv", index=False)

        docs = pd.DataFrame(POLICY_DOCS, columns=["document_id", "country", "source_name", "document_type", "title", "date", "text"])
        docs.to_csv(sample / "policy_documents_raw.csv", index=False)
    ''')

    write("src/data/clean_reactor_data.py", """
    from __future__ import annotations

    import re
    import numpy as np
    import pandas as pd
    from src import config
    from src.utils.constants import REGIONS, STATUS_GROUPS, TECHNOLOGY_FAMILY

    def _num(x):
        if pd.isna(x):
            return np.nan
        return float(str(x).replace(",", "").strip())

    def standardize_status(status: str) -> str:
        s = re.sub(r"[-_]+", " ", str(status).strip().lower())
        return STATUS_GROUPS.get(s, STATUS_GROUPS.get(s.replace("  ", " "), str(status).strip().title()))

    def standardize_reactor_type(raw: str, design: str | None = None) -> str:
        text = f"{raw} {design or ''}".upper()
        if "AP1000" in text: return "AP1000"
        if "EPR" in text: return "EPR"
        if "VVER" in text: return "VVER"
        if "APR1400" in text: return "PWR"
        if "BWRX" in text or "SMR" in text or "CAREM" in text: return "SMR-LWR"
        if "PHWR" in text or "CANDU" in text: return "PHWR"
        if "BWR" in text: return "BWR"
        if "SFR" in text or "NATRIUM" in text: return "SFR"
        if "FBR" in text or "BN-" in text: return "FBR"
        if "MSR" in text or "MOLTEN" in text: return "MSR"
        if "HTGR" in text or "HTR" in text: return "HTGR"
        return str(raw).strip().upper()

    def clean_reactors() -> pd.DataFrame:
        path = config.RAW / "sample" / "dirty_reactors_raw.csv"
        df = pd.read_csv(path)
        df["reactor_name"] = df["reactor_name"].astype(str).str.strip()
        df["reactor_id"] = (
            df["country"].astype(str).str.upper().str[:3] + "-" +
            df["plant_name"].astype(str).str.upper().str.replace(r"[^A-Z0-9]+", "-", regex=True) + "-" +
            df["unit_name"].astype(str).str.upper().str.replace(r"[^A-Z0-9]+", "-", regex=True)
        )
        df["net_capacity_mwe"] = df["net_capacity_mwe"].map(_num)
        df["gross_capacity_mwe"] = df["gross_capacity_mwe"].map(_num)
        df["capacity_mwe"] = df["net_capacity_mwe"].fillna(df["gross_capacity_mwe"])
        df["status_group"] = df["status"].map(standardize_status)
        df["status"] = df["status"].astype(str).str.strip().str.replace("-", " ").str.title()
        df["reactor_type_standardized"] = [standardize_reactor_type(r, d) for r, d in zip(df["reactor_type"], df["design_name"])]
        df["technology_family"] = df["reactor_type_standardized"].map(TECHNOLOGY_FAMILY).fillna("Other/Unclassified")
        df["generation_category"] = np.select(
            [
                df["reactor_type_standardized"].isin(["AP1000", "EPR", "VVER", "PWR"]),
                df["reactor_type_standardized"].isin(["SMR-LWR", "SFR", "MSR", "HTGR", "FBR"]),
            ],
            ["Gen III/III+ or modern LWR", "Advanced/Gen IV candidate"],
            default="Gen II/legacy or unspecified",
        )
        df["size_category"] = pd.cut(df["capacity_mwe"], bins=[0, 50, 300, 700, 2000], labels=["Micro/small", "SMR", "Mid-size", "Large"], include_lowest=True).astype(str)
        for col in ["construction_start_date", "grid_connection_date", "commercial_operation_date", "shutdown_date"]:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        df["construction_start_year"] = df["construction_start_date"].dt.year
        df["expected_start_year"] = np.where(df["status_group"].isin(["Construction", "Planned", "Proposed"]), np.nan, df["commercial_operation_date"].dt.year)
        df["age_years"] = np.where(df["commercial_operation_date"].notna(), config.CURRENT_YEAR - df["commercial_operation_date"].dt.year, np.nan)
        df["region"] = df["country"].map(REGIONS).fillna("Other")
        df["source_confidence"] = np.where(df["source_name"].str.contains("Sample", case=False, na=False), 0.55, 0.8)
        df["source_last_updated"] = "2026-05-17"
        df = df.sort_values(["source_confidence", "reactor_id"], ascending=[False, True]).drop_duplicates("reactor_id", keep="first")
        cols = [
            "reactor_id","reactor_name","unit_name","plant_name","country","region","latitude","longitude",
            "status","status_group","reactor_type","reactor_type_standardized","technology_family",
            "generation_category","size_category","capacity_mwe","gross_capacity_mwe","net_capacity_mwe",
            "construction_start_date","grid_connection_date","commercial_operation_date","shutdown_date",
            "expected_start_year","age_years","owner","operator","vendor","source_name","source_confidence",
            "source_last_updated"
        ]
        out = df[cols]
        out.to_csv(config.PROCESSED / "reactors_master.csv", index=False)
        return out
    """)

    write("src/data/clean_country_data.py", """
    from __future__ import annotations

    import pandas as pd
    from src import config

    def clean_country_context() -> pd.DataFrame:
        df = pd.read_csv(config.RAW / "sample" / "dirty_country_context_raw.csv")
        df["nuclear_generation_twh"] = df["electricity_generation_twh"] * df["nuclear_share_fraction"]
        df["nuclear_share_percent"] = df["nuclear_share_fraction"] * 100
        out = df.drop(columns=["nuclear_share_fraction"])
        out.to_csv(config.INTERIM / "country_context.csv", index=False)
        return out
    """)

    write("src/features/technology_features.py", """
    from __future__ import annotations

    import numpy as np
    import pandas as pd
    from src import config

    TAXONOMY = [
        ["Light Water Reactor","PWR","water","water","thermal","once-through/LEU","uranium oxide","Gen II/III/III+",95,"commercial",False,False,False,False,False],
        ["Light Water Reactor","BWR","water","water","thermal","once-through/LEU","uranium oxide","Gen II/III",90,"commercial",False,False,False,False,False],
        ["Heavy Water Reactor","PHWR","heavy water","heavy water","thermal","natural uranium/LEU","uranium oxide","Gen II/III",88,"commercial",False,False,False,False,False],
        ["Light Water Reactor","VVER","water","water","thermal","once-through/LEU","uranium oxide","Gen III/III+",90,"commercial",False,False,False,False,False],
        ["Light Water Reactor","EPR","water","water","thermal","once-through/LEU","uranium oxide","Gen III+",82,"commercializing",False,False,False,False,False],
        ["Light Water Reactor","AP1000","water","water","thermal","once-through/LEU","uranium oxide","Gen III+",85,"commercializing",False,False,False,False,False],
        ["Small Modular Reactor","SMR-LWR","water","water","thermal","once-through/LEU/HALEU possible","uranium oxide","SMR/Gen III+",48,"first deployment",True,False,False,False,False],
        ["Gas-Cooled Reactor","HTGR","helium","graphite","thermal","LEU/HALEU","TRISO","Gen IV candidate",42,"demonstration/early commercial",True,True,False,False,False],
        ["Fast Reactor","SFR","sodium","none","fast","closed fuel cycle possible","MOX/metal","Gen IV candidate",45,"limited operating experience",False,True,False,False,True],
        ["Fast Reactor","LFR","lead/lead-bismuth","none","fast","closed fuel cycle possible","nitride/metal","Gen IV candidate",25,"concept/licensing",True,True,False,False,True],
        ["Molten Salt Reactor","MSR","molten salt","graphite/none","thermal/fast","thorium or uranium possible","liquid fuel/salt","Gen IV candidate",22,"concept/demonstration",True,True,True,True,False],
        ["Thorium Fuel Cycle","Thorium concepts","varies","varies","thermal/fast","thorium/U-233","thorium-bearing","advanced fuel cycle",18,"R&D/concept",False,True,True,False,False],
        ["Microreactor","Microreactor","varies","varies","thermal/fast","HALEU likely","TRISO/metal","advanced",20,"prototype/concept",True,True,False,False,False],
    ]

    def build_technology_taxonomy(reactors: pd.DataFrame) -> pd.DataFrame:
        cols = ["technology_family","reactor_type","coolant","moderator","neutron_spectrum","fuel_cycle","fuel_type","generation_category","base_maturity","deployment_status","smr_flag","geniv_flag","thorium_potential_flag","molten_salt_flag","fast_reactor_flag"]
        tax = pd.DataFrame(TAXONOMY, columns=cols)
        counts = reactors.groupby("reactor_type_standardized").agg(
            known_operating_units=("status_group", lambda s: int((s == "Operating").sum())),
            known_under_construction_units=("status_group", lambda s: int((s == "Construction").sum())),
        ).reset_index().rename(columns={"reactor_type_standardized": "reactor_type"})
        tax = tax.merge(counts, on="reactor_type", how="left").fillna({"known_operating_units": 0, "known_under_construction_units": 0})
        tax["maturity_score"] = np.clip(tax["base_maturity"] + tax["known_operating_units"] * 1.2 + tax["known_under_construction_units"] * 1.8, 0, 100).round(1)
        tax["commercial_maturity_level"] = pd.cut(tax["maturity_score"], bins=[0, 30, 55, 75, 100], labels=["early-stage", "demonstration", "commercializing", "commercial"], include_lowest=True).astype(str)
        tax["notes"] = "Score combines public deployment status, units in sample pipeline, novelty and regulatory familiarity. Sample-linked counts are illustrative until real data is ingested."
        out = tax.drop(columns=["base_maturity"])
        out.to_csv(config.PROCESSED / "technology_taxonomy.csv", index=False)
        return out
    """)

    write("src/features/reactor_features.py", """
    from __future__ import annotations
    import pandas as pd

    def add_reactor_feature_flags(df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        text = (out["reactor_type_standardized"].fillna("") + " " + out["technology_family"].fillna("")).str.upper()
        out["smr_flag"] = text.str.contains("SMR|SMALL MODULAR|MICRO")
        out["geniv_flag"] = text.str.contains("SFR|LFR|MSR|HTGR|FAST|MOLTEN|GEN IV|MICRO")
        out["molten_salt_flag"] = text.str.contains("MSR|MOLTEN")
        out["thorium_potential_flag"] = text.str.contains("THORIUM|MSR")
        out["fast_reactor_flag"] = text.str.contains("SFR|LFR|FBR|FAST")
        return out
    """)

    write("src/features/pipeline_features.py", """
    from __future__ import annotations
    import numpy as np
    import pandas as pd
    from src import config

    def build_reactor_pipeline(reactors: pd.DataFrame, taxonomy: pd.DataFrame, countries: pd.DataFrame) -> pd.DataFrame:
        df = reactors[reactors["status_group"].isin(["Construction", "Planned", "Proposed", "Paused"])].copy()
        tax = taxonomy[["reactor_type","maturity_score"]].rename(columns={"reactor_type":"reactor_type_standardized"})
        df = df.merge(tax, on="reactor_type_standardized", how="left")
        df = df.merge(countries[["country","gdp_current_usd","nuclear_experience_years","historical_completed_reactors"]], on="country", how="left")
        if "construction_start_year" not in df.columns:
            df["construction_start_year"] = pd.to_datetime(df["construction_start_date"], errors="coerce").dt.year
        stage_score = df["status_group"].map({"Construction": 85, "Planned": 55, "Proposed": 30, "Paused": 20}).fillna(35)
        experience = np.clip(df["nuclear_experience_years"].fillna(0) / 70 * 100, 0, 100)
        tech = df["maturity_score"].fillna(35)
        gdp = np.clip(np.log10(df["gdp_current_usd"].fillna(1)) / 14 * 100, 0, 100)
        df["project_maturity_score"] = (0.45 * stage_score + 0.25 * tech + 0.20 * experience + 0.10 * gdp).round(1)
        df["delay_risk_score"] = (100 - df["project_maturity_score"] + np.where(df["capacity_mwe"] > 1200, 7, 0) + np.where(df["status_group"].eq("Proposed"), 8, 0)).clip(0, 100).round(1)
        df["realization_probability"] = (df["project_maturity_score"] / 100).clip(0.05, 0.95).round(2)
        df["expected_operation_year"] = np.select(
            [df["status_group"].eq("Construction"), df["status_group"].eq("Planned"), df["status_group"].eq("Proposed")],
            [2030, 2035, 2042],
            default=2045,
        )
        df["delay_years_if_known"] = np.where(df["construction_start_year"].notna(), np.maximum(0, config.CURRENT_YEAR - df["construction_start_year"] - 7), np.nan)
        df["project_stage"] = df["status_group"]
        df["project_id"] = "PIPE-" + df["reactor_id"].astype(str)
        cols = ["project_id","reactor_name","country","status","status_group","technology_family","reactor_type_standardized","capacity_mwe","construction_start_year","expected_operation_year","delay_years_if_known","project_stage","project_maturity_score","delay_risk_score","realization_probability","source_name"]
        out = df[cols].rename(columns={"reactor_type_standardized":"reactor_type"})
        out.to_csv(config.PROCESSED / "reactor_pipeline.csv", index=False)
        return out
    """)

    write("src/features/country_features.py", """
    from __future__ import annotations
    import numpy as np
    import pandas as pd
    from src import config

    def build_country_profiles(reactors: pd.DataFrame, context: pd.DataFrame, pipeline: pd.DataFrame) -> pd.DataFrame:
        grouped = reactors.groupby("country").agg(
            operating_reactor_count=("status_group", lambda s: int((s == "Operating").sum())),
            construction_reactor_count=("status_group", lambda s: int((s == "Construction").sum())),
            planned_reactor_count=("status_group", lambda s: int((s == "Planned").sum())),
            proposed_reactor_count=("status_group", lambda s: int((s == "Proposed").sum())),
            operating_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Operating")].sum())),
            construction_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Construction")].sum())),
            planned_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Planned")].sum())),
            proposed_capacity_mwe=("capacity_mwe", lambda x: float(x[reactors.loc[x.index, "status_group"].eq("Proposed")].sum())),
            average_fleet_age=("age_years", "mean"),
        ).reset_index()
        out = context.merge(grouped, on="country", how="outer")
        out["region"] = out["region"].ffill()
        numeric = [c for c in out.columns if c.endswith("_count") or c.endswith("_mwe") or c in ["average_fleet_age"]]
        out[numeric] = out[numeric].fillna(0)
        flags = pipeline.groupby("country").agg(
            smr_interest_flag=("technology_family", lambda s: bool(s.str.contains("Small Modular|Micro", case=False, na=False).any())),
            geniv_interest_flag=("technology_family", lambda s: bool(s.str.contains("Fast|Molten|Gas|Micro", case=False, na=False).any())),
        ).reset_index()
        out = out.merge(flags, on="country", how="left").fillna({"smr_interest_flag": False, "geniv_interest_flag": False})
        out["advanced_reactor_activity_score"] = (
            out["smr_interest_flag"].astype(int) * 35 + out["geniv_interest_flag"].astype(int) * 35 +
            np.clip(out["planned_capacity_mwe"].fillna(0) / 3000 * 30, 0, 30)
        ).round(1)
        out["policy_signal_score"] = np.clip(35 + out["advanced_reactor_activity_score"] * 0.4 + out["planned_reactor_count"] * 5 + out["construction_reactor_count"] * 8, 0, 100).round(1)
        out["electricity_demand_twh"] = out["electricity_generation_twh"]
        out.to_csv(config.PROCESSED / "country_nuclear_profile.csv", index=False)
        return out
    """)

    write("src/features/scenario_features.py", """
    from __future__ import annotations
    import pandas as pd
    from src import config

    def build_capacity_scenarios(country: pd.DataFrame, pipeline: pd.DataFrame) -> pd.DataFrame:
        years = [2030, 2040, 2050]
        scenarios = {"Conservative": 0.55, "Base": 0.75, "Accelerated": 0.95}
        rows = []
        for _, c in country.iterrows():
            base_gwe = c.get("operating_capacity_mwe", 0) / 1000
            demand = c.get("electricity_demand_twh", 0)
            p = pipeline[pipeline["country"] == c["country"]]
            for year in years:
                eligible = p[p["expected_operation_year"] <= year]
                for scen, adj in scenarios.items():
                    add_gwe = (eligible["capacity_mwe"] * eligible["realization_probability"] * adj).sum() / 1000
                    cap = base_gwe + add_gwe
                    cf = 0.86
                    gen = cap * cf * 8.76
                    smr = eligible[eligible["technology_family"].str.contains("Small Modular|Micro", case=False, na=False)]["capacity_mwe"].sum() / 1000 * adj
                    geniv = eligible[eligible["technology_family"].str.contains("Fast|Molten|Gas", case=False, na=False)]["capacity_mwe"].sum() / 1000 * adj
                    rows.append({
                        "year": year, "country": c["country"], "region": c.get("region"), "scenario": scen,
                        "capacity_gwe": round(cap, 3), "capacity_factor": cf,
                        "estimated_generation_twh": round(gen, 2),
                        "nuclear_share_estimate": round((gen / demand * 100) if demand else 0, 2),
                        "smr_capacity_gwe": round(smr, 3), "geniv_capacity_gwe": round(geniv, 3),
                        "large_reactor_capacity_gwe": round(max(cap - smr - geniv, 0), 3),
                        "source_name": "Scenario engine using processed reactor pipeline and sample/ingested context",
                    })
        out = pd.DataFrame(rows)
        out.to_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv", index=False)
        out.to_csv(config.PREDICTIONS / "electricity_supply_scenarios.csv", index=False)
        return out
    """)

    write("src/data/integrate_sources.py", """
    from __future__ import annotations

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
        reactors.to_csv(__import__("src.config").config.PROCESSED / "reactors_master.csv", index=False)
        return reactors, countries, pipeline, taxonomy, scenarios
    """)

    write("src/data/data_quality_checks.py", """
    from __future__ import annotations

    import json
    import pandas as pd
    from src import config

    def run_data_quality_checks(reactors: pd.DataFrame, countries: pd.DataFrame) -> dict:
        missing = reactors.isna().mean().sort_values(ascending=False).round(3).to_dict()
        coverage = reactors.groupby("country").size().sort_values(ascending=False).to_dict()
        duplicates = int(reactors.duplicated("reactor_id").sum())
        confidence = reactors.groupby("source_name")["source_confidence"].mean().round(2).to_dict()
        quality = {
            "reactor_rows": int(len(reactors)),
            "country_rows": int(len(countries)),
            "duplicate_reactor_ids": duplicates,
            "missing_fraction_by_field": missing,
            "source_confidence": confidence,
            "source_coverage_by_country": coverage,
            "sample_data_warning": "Raw fallback data is labeled sample-only and is intended to be replaced or augmented by manual/official source exports.",
        }
        (config.METRICS / "data_quality_metrics.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
        pd.DataFrame({"field": list(missing), "missing_fraction": list(missing.values())}).to_csv(config.ANALYTICS / "missingness_by_field.csv", index=False)
        return quality
    """)

    write("src/models/capacity_forecasting_xgboost.py", """
    from __future__ import annotations

    import json
    import numpy as np
    import pandas as pd
    from joblib import dump
    from sklearn.compose import ColumnTransformer
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    try:
        from xgboost import XGBRegressor
    except Exception:
        XGBRegressor = None
    from sklearn.ensemble import RandomForestRegressor
    from src import config

    def train_capacity_forecaster(countries: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        df = countries.copy()
        df["target_capacity_2035_mwe"] = df["operating_capacity_mwe"] + 0.75 * df["construction_capacity_mwe"] + 0.45 * df["planned_capacity_mwe"] + 0.15 * df["proposed_capacity_mwe"]
        features = ["region","income_group","gdp_current_usd","population","electricity_generation_twh","nuclear_share_percent","operating_capacity_mwe","construction_capacity_mwe","planned_capacity_mwe","proposed_capacity_mwe","average_fleet_age","nuclear_experience_years","policy_signal_score"]
        X, y = df[features], df["target_capacity_2035_mwe"]
        numeric = [c for c in features if c not in ["region","income_group"]]
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["region","income_group"]), ("num", StandardScaler(), numeric)])
        model = XGBRegressor(n_estimators=80, max_depth=3, learning_rate=0.08, objective="reg:squarederror", random_state=42) if XGBRegressor else RandomForestRegressor(n_estimators=120, random_state=42)
        pipe = Pipeline([("preprocess", pre), ("model", model)])
        if len(df) >= 8:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)
        else:
            X_train, X_test, y_train, y_test = X, X, y, y
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        metrics = {
            "model_name": "capacity_forecast_xgboost_or_rf",
            "model_type": "XGBoostRegressor" if XGBRegressor else "RandomForestRegressor fallback",
            "target": "heuristic expected capacity by 2035 from current fleet and pipeline",
            "mae": float(mean_absolute_error(y_test, pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
            "r2": float(r2_score(y_test, pred)) if len(y_test) > 1 else None,
            "notes": "Portfolio sample target is scenario-derived. Replace with historical snapshots for production validation.",
        }
        df["forecast_capacity_2035_mwe"] = pipe.predict(X).round(1)
        out = df[["country","region","forecast_capacity_2035_mwe","target_capacity_2035_mwe","policy_signal_score"]]
        out.to_csv(config.PREDICTIONS / "capacity_forecasts.csv", index=False)
        (config.METRICS / "forecasting_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        dump(pipe, config.MODELS / "capacity_forecast_xgboost.joblib")
        return out, metrics
    """)

    write("src/models/capacity_forecasting_statsmodels.py", """
    from __future__ import annotations
    import json
    import pandas as pd
    from src import config

    def run_statsmodels_global_forecast(reactors: pd.DataFrame) -> pd.DataFrame:
        rows = []
        operating = reactors[reactors["commercial_operation_date"].notna()].copy()
        operating["year"] = pd.to_datetime(operating["commercial_operation_date"]).dt.year
        annual = operating.groupby("year")["capacity_mwe"].sum().sort_index().cumsum()
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            if len(annual) >= 4:
                model = ExponentialSmoothing(annual, trend="add", seasonal=None).fit()
                fc = model.forecast(10)
            else:
                raise ValueError("Not enough annual observations")
        except Exception:
            last = annual.iloc[-1] if len(annual) else 0
            avg = annual.diff().dropna().tail(5).mean() if len(annual) > 1 else 1000
            fc = pd.Series({y: last + (i + 1) * avg for i, y in enumerate(range(2027, 2037))})
        out = pd.DataFrame({"year": fc.index.astype(int), "global_capacity_mwe_forecast": fc.values})
        out.to_csv(config.PREDICTIONS / "statsmodels_global_capacity_forecast.csv", index=False)
        return out
    """)

    write("src/models/project_realization_classifier.py", """
    from __future__ import annotations
    import json
    import numpy as np
    import pandas as pd
    from joblib import dump
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    try:
        from xgboost import XGBClassifier
    except Exception:
        XGBClassifier = None
    from src import config

    def train_project_realization_models(pipeline_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        df = pipeline_df.copy()
        df["label_high_realization"] = (df["realization_probability"] >= 0.6).astype(int)
        features = ["status_group","technology_family","reactor_type","capacity_mwe","project_maturity_score","delay_risk_score"]
        X, y = df[features], df["label_high_realization"]
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["status_group","technology_family","reactor_type"]), ("num", StandardScaler(), ["capacity_mwe","project_maturity_score","delay_risk_score"])])
        candidates = {
            "logistic_regression": LogisticRegression(max_iter=1000),
            "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
        }
        if XGBClassifier:
            candidates["xgboost_classifier"] = XGBClassifier(n_estimators=60, max_depth=3, learning_rate=0.1, eval_metric="logloss", random_state=42)
        metrics = {}
        best_name, best_pipe, best_f1 = None, None, -1
        stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42, stratify=stratify) if len(df) >= 6 else (X, X, y, y)
        for name, model in candidates.items():
            pipe = Pipeline([("preprocess", pre), ("model", model)])
            pipe.fit(X_train, y_train)
            pred = pipe.predict(X_test)
            prob = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") and y_test.nunique() > 1 else pred
            m = {
                "accuracy": float(accuracy_score(y_test, pred)),
                "precision": float(precision_score(y_test, pred, zero_division=0)),
                "recall": float(recall_score(y_test, pred, zero_division=0)),
                "f1": float(f1_score(y_test, pred, zero_division=0)),
                "roc_auc": float(roc_auc_score(y_test, prob)) if y_test.nunique() > 1 else None,
                "notes": "Labels are derived from transparent heuristic scoring because public historical realization labels are insufficient in the sample build.",
            }
            metrics[name] = m
            if m["f1"] > best_f1:
                best_name, best_pipe, best_f1 = name, pipe, m["f1"]
        df["risk_level"] = pd.cut(df["delay_risk_score"], bins=[0, 35, 65, 100], labels=["Low", "Medium", "High"], include_lowest=True).astype(str)
        df["realization_label"] = pd.cut(df["realization_probability"], bins=[0, 0.4, 0.7, 1], labels=["Low", "Medium", "High"], include_lowest=True).astype(str)
        out = df[["project_id","reactor_name","country","technology_family","capacity_mwe","delay_risk_score","risk_level","realization_probability","realization_label","project_maturity_score"]]
        out.to_csv(config.PREDICTIONS / "project_risk_scores.csv", index=False)
        (config.METRICS / "risk_model_metrics.json").write_text(json.dumps({"best_model": best_name, "models": metrics}, indent=2), encoding="utf-8")
        dump(best_pipe, config.MODELS / "project_realization_classifier.joblib")
        dump(best_pipe, config.MODELS / "delay_risk_model.joblib")
        return out, metrics
    """)

    write("src/models/technology_maturity_score.py", """
    from __future__ import annotations
    import json
    import pandas as pd
    from joblib import dump
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from src import config

    def score_technology_maturity(taxonomy: pd.DataFrame):
        df = taxonomy.copy()
        df["maturity_label"] = pd.cut(df["maturity_score"], bins=[0,30,55,75,100], labels=["Early", "Demonstration", "Commercializing", "Commercial"], include_lowest=True).astype(str)
        df["technology_risk_label"] = pd.cut(100 - df["maturity_score"], bins=[0,25,50,75,100], labels=["Low", "Medium", "High", "Very High"], include_lowest=True).astype(str)
        df["explanation"] = df.apply(lambda r: f"{r.reactor_type}: {r.deployment_status}; maturity reflects deployment, novelty, regulatory familiarity and sample pipeline counts.", axis=1)
        out = df[["technology_family","reactor_type","maturity_score","maturity_label","technology_risk_label","explanation"]]
        out.to_csv(config.PREDICTIONS / "technology_maturity_scores.csv", index=False)
        summary = {"average_maturity_score": float(df["maturity_score"].mean()), "lowest_maturity": df.sort_values("maturity_score").head(3)["reactor_type"].tolist(), "highest_maturity": df.sort_values("maturity_score", ascending=False).head(3)["reactor_type"].tolist()}
        (config.METRICS / "technology_maturity_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["technology_family","reactor_type","coolant","moderator","deployment_status"])], remainder="passthrough")
        features = ["technology_family","reactor_type","coolant","moderator","deployment_status","smr_flag","geniv_flag","known_operating_units","known_under_construction_units"]
        model = Pipeline([("preprocess", pre), ("model", RandomForestRegressor(n_estimators=80, random_state=42))])
        model.fit(df[features], df["maturity_score"])
        dump(model, config.MODELS / "technology_maturity_model.joblib")
        return out, summary
    """)

    write("src/models/country_clustering.py", """
    from __future__ import annotations
    import json
    import pandas as pd
    from joblib import dump
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from src import config

    CLUSTER_NAMES = {
        0: "Mature or legacy fleet",
        1: "High-growth builder",
        2: "Emerging nuclear entrant",
        3: "Advanced technology explorer",
    }

    def cluster_countries(countries: pd.DataFrame):
        features = ["operating_capacity_mwe","construction_capacity_mwe","planned_capacity_mwe","proposed_capacity_mwe","nuclear_share_percent","gdp_current_usd","electricity_generation_twh","population","average_fleet_age","advanced_reactor_activity_score","policy_signal_score"]
        X = countries[features].fillna(0)
        n = min(4, max(2, len(countries) // 4))
        pipe = Pipeline([("scale", StandardScaler()), ("kmeans", KMeans(n_clusters=n, random_state=42, n_init=10))])
        labels = pipe.fit_predict(X)
        coords = PCA(n_components=2, random_state=42).fit_transform(StandardScaler().fit_transform(X))
        out = countries[["country","region"]].copy()
        out["cluster_id"] = labels
        out["cluster_name"] = out["cluster_id"].map(CLUSTER_NAMES).fillna("Nuclear strategy segment")
        out["pca_x"], out["pca_y"] = coords[:,0], coords[:,1]
        out.to_csv(config.PREDICTIONS / "country_clusters.csv", index=False)
        metrics = {"n_clusters": int(n), "silhouette_score": float(silhouette_score(StandardScaler().fit_transform(X), labels)) if n > 1 and len(set(labels)) > 1 else None}
        (config.METRICS / "clustering_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        dump(pipe, config.MODELS / "country_clustering_model.joblib")
        return out, metrics
    """)

    write("src/models/electricity_supply_scenarios.py", """
    from __future__ import annotations
    import pandas as pd

    def estimate_generation_twh(capacity_gw: float, capacity_factor: float) -> float:
        return capacity_gw * capacity_factor * 8.76

    def add_value_proxy(df: pd.DataFrame, price_per_mwh: float = 75.0) -> pd.DataFrame:
        out = df.copy()
        out["estimated_mwh"] = out["estimated_generation_twh"] * 1_000_000
        out["price_per_mwh"] = price_per_mwh
        out["estimated_market_value_usd"] = out["estimated_mwh"] * price_per_mwh
        return out
    """)

    write("src/models/revenue_value_scenarios.py", """
    from src.models.electricity_supply_scenarios import add_value_proxy
    """)

    write("src/models/model_evaluation.py", """
    from __future__ import annotations
    import pandas as pd
    from src import config

    def write_model_metrics_table(forecast_metrics: dict, risk_metrics: dict) -> pd.DataFrame:
        rows = [{
            "model_name": forecast_metrics.get("model_name"),
            "model_type": forecast_metrics.get("model_type"),
            "target": forecast_metrics.get("target"),
            "mae": forecast_metrics.get("mae"),
            "rmse": forecast_metrics.get("rmse"),
            "mape": None, "accuracy": None, "precision": None, "recall": None, "f1": None, "roc_auc": None,
            "notes": forecast_metrics.get("notes"),
        }]
        for name, m in risk_metrics.items():
            rows.append({"model_name": name, "model_type": "classifier", "target": "high realization label", "mae": None, "rmse": None, "mape": None, "accuracy": m.get("accuracy"), "precision": m.get("precision"), "recall": m.get("recall"), "f1": m.get("f1"), "roc_auc": m.get("roc_auc"), "notes": m.get("notes")})
        df = pd.DataFrame(rows)
        df.to_csv(config.PROCESSED / "model_metrics.csv", index=False)
        return df
    """)

    write("src/nlp/nuclear_text_cleaning.py", """
    from __future__ import annotations
    import re

    def clean_text(text: str) -> str:
        text = str(text).lower()
        text = re.sub(r"[^a-z0-9\\s-]", " ", text)
        return re.sub(r"\\s+", " ", text).strip()
    """)
    write("src/nlp/keyword_extraction.py", """
    from __future__ import annotations
    from collections import Counter
    import pandas as pd
    from src.nlp.nuclear_text_cleaning import clean_text

    DEFAULT_STOPWORDS = set("the and of to in for with a an is are be as by or on from this that into it at".split())

    def tokenize(text: str) -> list[str]:
        try:
            import nltk
            from nltk.corpus import stopwords
            try:
                stops = set(stopwords.words("english"))
            except LookupError:
                stops = DEFAULT_STOPWORDS
        except Exception:
            stops = DEFAULT_STOPWORDS
        return [t for t in clean_text(text).split() if len(t) > 2 and t not in stops]

    def extract_keywords(docs: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for _, row in docs.iterrows():
            counts = Counter(tokenize(row["text"]))
            for term, count in counts.most_common(20):
                rows.append({"document_id": row["document_id"], "country": row["country"], "term": term, "count": count})
        return pd.DataFrame(rows)
    """)
    write("src/nlp/topic_tagging.py", """
    from __future__ import annotations

    TOPICS = {
        "SMR": ["smr", "small modular", "bwrx", "carem", "microreactor"],
        "Gen IV": ["gen iv", "advanced reactor", "high temperature", "fast reactor", "closed fuel"],
        "Molten Salt": ["molten salt", "msr", "salt"],
        "Thorium": ["thorium", "u-233"],
        "Fast Reactor": ["fast reactor", "sodium", "lead-cooled", "mox"],
        "Financing": ["financing", "finance", "investment", "cost"],
        "Delay Risk": ["delay", "licensing", "supply chain", "construction"],
        "Energy Security": ["energy security", "reliability", "coal replacement"],
        "Decarbonization": ["clean", "decarbonization", "emissions", "net zero"],
        "Industrial Heat": ["industrial heat", "hydrogen", "desalination", "process heat", "data center"],
    }

    def tag_topics(text: str) -> dict[str, int]:
        t = str(text).lower()
        return {topic: int(any(k in t for k in keys)) for topic, keys in TOPICS.items()}
    """)
    write("src/nlp/policy_signal_scoring.py", """
    from __future__ import annotations
    import pandas as pd
    from src import config
    from src.nlp.keyword_extraction import extract_keywords
    from src.nlp.topic_tagging import tag_topics

    def run_nlp_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
        docs = pd.read_csv(config.RAW / "sample" / "policy_documents_raw.csv")
        topic_rows = []
        enriched = []
        for _, row in docs.iterrows():
            tags = tag_topics(row["text"])
            score = min(100, 20 + sum(tags.values()) * 9)
            enriched.append({**row.to_dict(), "extracted_keywords": "", "detected_topics": ",".join([k for k,v in tags.items() if v]), "smr_signal": tags["SMR"], "geniv_signal": tags["Gen IV"], "financing_signal": tags["Financing"], "policy_support_signal": score, "delay_risk_signal": tags["Delay Risk"], "sentiment_or_policy_score": score})
            for topic, val in tags.items():
                topic_rows.append({"document_id": row["document_id"], "country": row["country"], "topic": topic, "present": val})
        docs_out = pd.DataFrame(enriched)
        kw = extract_keywords(docs)
        top_kw = kw.groupby(["country","term"], as_index=False)["count"].sum().sort_values("count", ascending=False)
        topics = pd.DataFrame(topic_rows)
        docs_out.to_csv(config.PROCESSED / "nlp_policy_documents.csv", index=False)
        kw.to_csv(config.ANALYTICS / "nlp_keywords.csv", index=False)
        top_kw.to_csv(config.ANALYTICS / "top_terms_by_country.csv", index=False)
        topics.to_csv(config.ANALYTICS / "topic_distribution.csv", index=False)
        topics.pivot_table(index="country", columns="topic", values="present", aggfunc="max", fill_value=0).to_csv(config.ANALYTICS / "country_policy_signals.csv")
        topics.to_csv(config.ANALYTICS / "technology_mentions.csv", index=False)
        return docs_out, topics
    """)
    write("src/nlp/nuclear_text_ingestion.py", "from src.nlp.policy_signal_scoring import run_nlp_pipeline\n")
    write("src/nlp/nlp_report.py", """
    from __future__ import annotations
    import pandas as pd

    def summarize_policy_signals(docs: pd.DataFrame) -> str:
        top = docs.sort_values("policy_support_signal", ascending=False).head(3)
        return "; ".join(f"{r.country}: {r.detected_topics}" for _, r in top.iterrows())
    """)

    write("src/eda/global_eda.py", """
    from __future__ import annotations
    import pandas as pd

    def country_capacity(reactors: pd.DataFrame) -> pd.DataFrame:
        return reactors[reactors["status_group"].eq("Operating")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
    """)
    write("src/eda/eda_report_generator.py", """
    from __future__ import annotations
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    from src import config
    from src.utils.plotting import set_theme

    def _bar(df, x, y, title, filename, top=15):
        fig, ax = plt.subplots(figsize=(10, 6))
        data = df.head(top).copy()
        sns.barplot(data=data, x=x, y=y, ax=ax)
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=40)
        fig.savefig(config.FIGURES / filename)
        plt.close(fig)

    def generate_eda_outputs(reactors: pd.DataFrame, countries: pd.DataFrame, pipeline: pd.DataFrame, taxonomy: pd.DataFrame, scenarios: pd.DataFrame, topics: pd.DataFrame) -> None:
        set_theme()
        cap = reactors[reactors.status_group.eq("Operating")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
        _bar(cap, "country", "capacity_mwe", "Operating Nuclear Capacity by Country", "global_capacity_by_country.png")
        cnt = reactors[reactors.status_group.eq("Operating")].groupby("country", as_index=False).size().sort_values("size", ascending=False)
        _bar(cnt, "country", "size", "Operating Reactors by Country", "operating_reactors_by_country.png")
        uc = pipeline[pipeline.status_group.eq("Construction")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
        _bar(uc, "country", "capacity_mwe", "Under Construction Capacity by Country", "under_construction_by_country.png")
        planned = pipeline[pipeline.status_group.eq("Planned")].groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False)
        _bar(planned, "country", "capacity_mwe", "Planned Capacity by Country", "planned_capacity_by_country.png")
        _bar(reactors.groupby("technology_family", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False), "technology_family", "capacity_mwe", "Technology Mix - Fleet", "technology_mix_operating.png")
        _bar(pipeline.groupby("technology_family", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False), "technology_family", "capacity_mwe", "Technology Mix - Pipeline", "technology_mix_pipeline.png")
        for col, title, file in [
            ("age_years","Reactor Age Distribution","reactor_age_distribution.png"),
            ("nuclear_generation_twh","Nuclear Generation Context","nuclear_generation_trend.png"),
            ("nuclear_share_percent","Nuclear Share by Country","nuclear_share_by_country.png"),
            ("maturity_score","SMR and Gen IV Maturity Matrix","smr_geniv_maturity_matrix.png"),
        ]:
            fig, ax = plt.subplots(figsize=(10,6))
            data = taxonomy if col == "maturity_score" else countries if col in countries.columns else reactors
            sns.histplot(data[col].dropna(), ax=ax)
            ax.set_title(title)
            fig.savefig(config.FIGURES / file); plt.close(fig)
        _bar(scenarios[scenarios.year.eq(2050)].groupby("scenario", as_index=False)["capacity_gwe"].sum(), "scenario", "capacity_gwe", "2050 Capacity Scenarios", "capacity_scenarios_2050.png")
        _bar(scenarios.groupby("scenario", as_index=False)["estimated_generation_twh"].sum(), "scenario", "estimated_generation_twh", "Estimated Generation Scenarios", "estimated_generation_scenarios.png")
        _bar(countries.sort_values("policy_signal_score", ascending=False), "country", "policy_signal_score", "Country Strategy Signal", "country_strategy_clusters.png")
        fig, ax = plt.subplots(figsize=(11,6)); sns.heatmap(reactors.isna(), cbar=False, ax=ax); ax.set_title("Data Quality Heatmap"); fig.savefig(config.FIGURES / "data_quality_heatmap.png"); plt.close(fig)
        _bar(reactors.groupby("source_name", as_index=False).size(), "source_name", "size", "Source Coverage", "source_coverage_map.png")
        _bar(pipeline.groupby("expected_operation_year", as_index=False)["capacity_mwe"].sum(), "expected_operation_year", "capacity_mwe", "Pipeline Timeline", "pipeline_timeline.png")
        if (config.ANALYTICS / "nlp_keywords.csv").exists():
            kw = pd.read_csv(config.ANALYTICS / "nlp_keywords.csv").groupby("term", as_index=False)["count"].sum().sort_values("count", ascending=False)
            _bar(kw, "term", "count", "Top Policy Keywords", "top_policy_keywords.png", top=20)
        topic_heat = topics.pivot_table(index="country", columns="topic", values="present", aggfunc="max", fill_value=0)
        fig, ax = plt.subplots(figsize=(12,7)); sns.heatmap(topic_heat, annot=True, cmap="Blues", ax=ax); ax.set_title("Technology Topic Heatmap"); fig.savefig(config.FIGURES / "technology_topic_heatmap.png"); plt.close(fig)
        extra_specs = [
            ("capacity_by_region.png", reactors.groupby("region", as_index=False)["capacity_mwe"].sum(), "region", "capacity_mwe", "Capacity by Region"),
            ("pipeline_by_region.png", pipeline.groupby("country", as_index=False)["capacity_mwe"].sum(), "country", "capacity_mwe", "Pipeline by Country"),
            ("risk_by_country.png", pipeline.groupby("country", as_index=False)["delay_risk_score"].mean(), "country", "delay_risk_score", "Average Delay Risk by Country"),
            ("maturity_by_technology.png", taxonomy.sort_values("maturity_score", ascending=False), "reactor_type", "maturity_score", "Maturity by Technology"),
            ("policy_signal_by_country.png", countries.sort_values("policy_signal_score", ascending=False), "country", "policy_signal_score", "Policy Signal by Country"),
        ]
        for file, data, x, y, title in extra_specs:
            _bar(data, x, y, title, file)
        report = f'''# Full EDA Report

## Executive Readout
This EDA is generated from the processed reactor, country, pipeline, scenario and NLP tables. In this repository build, raw sample data is intentionally dirty and clearly labeled; official/manual exports can be added through the documented adapters.

## Data Quality
- Reactor rows: {len(reactors)}
- Countries represented: {reactors['country'].nunique()}
- Duplicate reactor IDs after cleaning: {reactors.duplicated('reactor_id').sum()}
- Main limitation: sample data demonstrates workflow and must not be treated as source-of-record.

## Global Fleet
Operating capacity is concentrated in countries with mature nuclear programs. The sample highlights the difference between operating capacity, under-construction capacity and early-stage planned/proposed capacity.

## Reactor Pipeline
Construction-stage projects receive higher realization scores than planned/proposed projects. Large first-of-a-kind projects and early advanced technologies receive higher delay-risk scores.

## Technology Mix
Commercial LWR families dominate maturity scoring. SMR, fast reactor, molten salt and thorium concepts are treated as strategic signals and scenario inputs, not deterministic near-term forecasts.

## Scenario Findings
The scenario engine translates capacity into TWh using capacity factor assumptions and project realization adjustments. This is a strategic planning tool, not an official forecast.

## NLP Signals
Policy text tagging detects SMR, Gen IV, financing, licensing/delay, energy security and decarbonization signals by country.
'''
        (config.OUTPUTS / "eda" / "full_eda_report.md").write_text(report, encoding="utf-8")
    """)
    for name in ["reactor_pipeline_eda.py","technology_mix_eda.py","country_eda.py","scenario_eda.py","data_quality_eda.py"]:
        write(f"src/eda/{name}", "from src.eda.eda_report_generator import generate_eda_outputs\n")

    write("src/sql/build_database.py", """
    from __future__ import annotations
    import sqlite3
    import pandas as pd
    from src import config

    TABLES = {
        "reactors": "reactors_master.csv",
        "countries": "country_nuclear_profile.csv",
        "technologies": "technology_taxonomy.csv",
        "pipeline_projects": "reactor_pipeline.csv",
        "capacity_scenarios": "nuclear_capacity_scenarios.csv",
        "model_metrics": "model_metrics.csv",
        "data_sources": "data_sources.csv",
        "policy_documents": "nlp_policy_documents.csv",
    }

    def build_sqlite_database() -> str:
        db = config.OUTPUTS / "nuclear_buildout.sqlite"
        with sqlite3.connect(db) as conn:
            for table, file in TABLES.items():
                path = config.PROCESSED / file
                if path.exists():
                    pd.read_csv(path).to_sql(table, conn, if_exists="replace", index=False)
            for table, path in {
                "forecasts": config.PREDICTIONS / "capacity_forecasts.csv",
                "project_risk_scores": config.PREDICTIONS / "project_risk_scores.csv",
                "technology_maturity_scores": config.PREDICTIONS / "technology_maturity_scores.csv",
                "nlp_topics": config.ANALYTICS / "topic_distribution.csv",
            }.items():
                if path.exists():
                    pd.read_csv(path).to_sql(table, conn, if_exists="replace", index=False)
        return str(db)
    """)

    write("src/sql/run_queries.py", """
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
    """)

    write("src/sql/export_powerbi_tables.py", """
    from __future__ import annotations
    import pandas as pd
    from src import config

    def export_powerbi_tables() -> list[str]:
        config.POWERBI.mkdir(parents=True, exist_ok=True)
        mapping = {
            "fact_reactors.csv": config.PROCESSED / "reactors_master.csv",
            "fact_reactor_pipeline.csv": config.PROCESSED / "reactor_pipeline.csv",
            "fact_capacity_scenarios.csv": config.PROCESSED / "nuclear_capacity_scenarios.csv",
            "fact_forecasts.csv": config.PREDICTIONS / "capacity_forecasts.csv",
            "fact_project_risk_scores.csv": config.PREDICTIONS / "project_risk_scores.csv",
            "fact_technology_maturity.csv": config.PREDICTIONS / "technology_maturity_scores.csv",
            "fact_nlp_policy_signals.csv": config.PROCESSED / "nlp_policy_documents.csv",
            "model_metrics.csv": config.PROCESSED / "model_metrics.csv",
        }
        written = []
        for out, src in mapping.items():
            if src.exists():
                df = pd.read_csv(src)
                df.to_csv(config.POWERBI / out, index=False)
                written.append(out)
        countries = pd.read_csv(config.PROCESSED / "country_nuclear_profile.csv")
        countries.to_csv(config.POWERBI / "dim_country.csv", index=False)
        countries[["region"]].drop_duplicates().to_csv(config.POWERBI / "dim_region.csv", index=False)
        pd.read_csv(config.PROCESSED / "technology_taxonomy.csv").to_csv(config.POWERBI / "dim_technology.csv", index=False)
        pd.DataFrame({"year": range(1950, 2051), "decade": [(y//10)*10 for y in range(1950, 2051)]}).to_csv(config.POWERBI / "dim_date.csv", index=False)
        return written
    """)

    write("sql/create_tables.sql", """
    -- SQLite schema is materialized by src/sql/build_database.py from processed CSV files.
    -- Tables: reactors, countries, technologies, pipeline_projects, capacity_scenarios,
    -- forecasts, project_risk_scores, technology_maturity_scores, policy_documents,
    -- nlp_topics, model_metrics, data_sources.
    """)
    for sql_file in ["reactor_queries.sql","country_queries.sql","technology_queries.sql","forecasting_queries.sql","risk_queries.sql","executive_queries.sql"]:
        write(f"sql/{sql_file}", "-- See src/sql/run_queries.py for executable query library.\n")

    write("src/reports/generate_executive_report.py", """
    from __future__ import annotations
    import os
    import pandas as pd
    from src import config

    DISCLAIMER = "This is a strategic analytics tool, not an official forecast or investment recommendation."

    def generate_executive_report() -> str:
        reactors = pd.read_csv(config.PROCESSED / "reactors_master.csv")
        countries = pd.read_csv(config.PROCESSED / "country_nuclear_profile.csv")
        pipeline = pd.read_csv(config.PROCESSED / "reactor_pipeline.csv")
        taxonomy = pd.read_csv(config.PROCESSED / "technology_taxonomy.csv")
        scenarios = pd.read_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv")
        risk = pd.read_csv(config.PREDICTIONS / "project_risk_scores.csv")
        top_growth = pipeline.groupby("country")["capacity_mwe"].sum().sort_values(ascending=False).head(5)
        report = f'''# Global Nuclear Buildout Intelligence Report

## 1. Executive Summary
The platform integrates reactor, country, technology, pipeline, scenario and policy-text analytics to evaluate where nuclear capacity may grow and what strategic risks affect the buildout. {DISCLAIMER}

## 2. Global Nuclear Buildout Overview
- Processed reactor/unit records: {len(reactors)}
- Countries represented: {reactors.country.nunique()}
- Operating capacity in processed table: {reactors.loc[reactors.status_group.eq("Operating"), "capacity_mwe"].sum():,.0f} MWe
- Construction capacity in processed table: {reactors.loc[reactors.status_group.eq("Construction"), "capacity_mwe"].sum():,.0f} MWe

## 3. Reactor Pipeline Analysis
Top pipeline countries by capacity: {", ".join([f"{c} ({v:,.0f} MWe)" for c, v in top_growth.items()])}.

## 4. Technology Mix Analysis
Commercial LWR technologies receive the highest maturity scores. Advanced reactor families are retained as scenario and maturity signals unless real deployment evidence supports forecasting.

## 5. SMR and Gen IV Watch
SMR/Gen IV scoring combines deployment stage, units operating/under construction, novelty, fuel/coolant complexity and source confidence. This avoids overstating early-stage technology certainty.

## 6. Country Strategy Clusters
Country clustering segments markets by operating capacity, pipeline, nuclear share, demand context, advanced-reactor activity and policy signal.

## 7. Forecasting Results
The forecasting table estimates near/mid-term capacity using pipeline and country features. It is a model demonstration and should be retrained with historical snapshots for production use.

## 8. Electricity Supply Scenarios
The scenario engine uses TWh/year = capacity_GW * capacity_factor * 8.76 and exposes capacity factor, realization probability and price assumptions.

## 9. Project Risk and Delay Analysis
Projects are scored with a transparent decision-support approach. High realization probabilities generally reflect construction status, mature technology and experienced nuclear countries.

## 10. Policy and NLP Signals
NLP tagging extracts signals for SMR, Gen IV, financing, licensing, energy security, decarbonization and industrial heat from curated public-text samples.

## 11. Business / Strategic Implications
The platform supports market screening, pipeline diligence, technology strategy, scenario planning and stakeholder reporting.

## 12. Data Limitations
Public nuclear data is fragmented. Planned/proposed project dates and advanced reactor deployment claims require careful source review. Sample data is not a source-of-record.

## 13. Recommended Next Steps
Replace sample rows with official/manual exports, add time-stamped project snapshots, validate risk labels against historical outcomes and connect Power BI/Streamlit to scheduled data refresh.

Sources used by this generated report: processed source registry, reactor master table, technology taxonomy, pipeline table, scenario table and NLP policy table.
'''
        path = config.REPORTS / "global_nuclear_buildout_report.md"
        path.write_text(report, encoding="utf-8")
        (config.REPORTS / "executive_summary.md").write_text(report.split("## 2.")[0], encoding="utf-8")
        return report
    """)

    write("src/reports/generate_model_card.py", """
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
    """)
    write("src/reports/generate_interview_brief.py", """
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
    """)
    write("src/reports/generate_eda_report.py", "from src.eda.eda_report_generator import generate_eda_outputs\n")
    write("src/reports/report_templates.py", "DISCLAIMER = 'This is a strategic analytics tool, not an official forecast or investment recommendation.'\n")

    write("src/dashboard/components/styling.py", """
    import streamlit as st

    def apply_style() -> None:
        st.markdown('''
        <style>
        :root { color-scheme: light; }
        .stApp { background: #f5f7fb; color: #17202a; }
        .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px; }
        .gnbi-header { border-bottom: 1px solid #cbd5e1; padding-bottom: .8rem; margin-bottom: 1.2rem; }
        .gnbi-title { font-size: 1.85rem; font-weight: 800; color: #0f172a; letter-spacing: 0; }
        .gnbi-subtitle { font-size: 1rem; color: #475569; margin-top: .25rem; }
        div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #d8e0ea; padding: .85rem .95rem; border-radius: 8px; box-shadow: 0 1px 2px rgba(15, 23, 42, .05); }
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        div[data-testid="stMetric"] div { color: #0f172a !important; }
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] { color: #64748b !important; font-size: .84rem; }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 1.55rem; font-weight: 800; }
        div[data-testid="stDataFrame"] { background: #ffffff; border-radius: 8px; }
        .stAlert { color: #0f172a; }
        h1, h2, h3, h4, h5, h6, p, label, span { color: inherit; }
        .small-note { font-size: .82rem; color: #64748b; }
        </style>
        ''', unsafe_allow_html=True)
    """)
    write("src/dashboard/components/filters.py", """
    import streamlit as st

    def multiselect_filter(label, values):
        vals = sorted([v for v in values if str(v) != "nan"])
        return st.sidebar.multiselect(label, vals, default=vals)
    """)
    write("src/dashboard/components/charts.py", """
    import plotly.express as px

    def bar(df, x, y, color=None, title=None):
        return px.bar(df, x=x, y=y, color=color, title=title, template="plotly_white")
    """)
    write("src/dashboard/components/metric_cards.py", """
    import streamlit as st

    def metric(label: str, value, help_text: str | None = None):
        st.metric(label, value, help=help_text)
    """)
    write("src/dashboard/components/maps.py", "import plotly.express as px\n")
    write("src/dashboard/components/tables.py", "import streamlit as st\n\ndef show(df):\n    st.dataframe(df, use_container_width=True)\n")

    write("src/dashboard/app.py", """
    from __future__ import annotations
    from pathlib import Path
    import sys
    import pandas as pd
    import streamlit as st
    import plotly.express as px

    ROOT = Path(__file__).resolve().parents[2]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from src import config
    from src.dashboard.components.styling import apply_style

    st.set_page_config(page_title="Global Nuclear Buildout Intelligence", layout="wide")
    apply_style()

    @st.cache_data
    def load_csv(path: Path) -> pd.DataFrame:
        return pd.read_csv(path) if path.exists() else pd.DataFrame()

    reactors = load_csv(config.PROCESSED / "reactors_master.csv")
    countries = load_csv(config.PROCESSED / "country_nuclear_profile.csv")
    pipeline = load_csv(config.PROCESSED / "reactor_pipeline.csv")
    taxonomy = load_csv(config.PROCESSED / "technology_taxonomy.csv")
    scenarios = load_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv")
    forecasts = load_csv(config.PREDICTIONS / "capacity_forecasts.csv")
    risk = load_csv(config.PREDICTIONS / "project_risk_scores.csv")
    clusters = load_csv(config.PREDICTIONS / "country_clusters.csv")
    docs = load_csv(config.PROCESSED / "nlp_policy_documents.csv")
    metrics = load_csv(config.PROCESSED / "model_metrics.csv")

    st.markdown('<div class="gnbi-header"><div class="gnbi-title">GLOBAL NUCLEAR BUILDOUT INTELLIGENCE PLATFORM</div><div class="gnbi-subtitle">Reactor Pipeline Forecasting, Technology Mix Scoring & Nuclear Electricity Supply Scenarios</div></div>', unsafe_allow_html=True)
    if reactors.empty:
        st.warning("Processed files are missing. Run `python run_pipeline.py` from the project root.")
        st.stop()

    st.sidebar.header("Global Filters")
    country_filter = st.sidebar.multiselect("Country", sorted(reactors.country.dropna().unique()), default=sorted(reactors.country.dropna().unique()))
    region_filter = st.sidebar.multiselect("Region", sorted(reactors.region.dropna().unique()), default=sorted(reactors.region.dropna().unique()))
    status_filter = st.sidebar.multiselect("Status group", sorted(reactors.status_group.dropna().unique()), default=sorted(reactors.status_group.dropna().unique()))
    tech_filter = st.sidebar.multiselect("Technology family", sorted(reactors.technology_family.dropna().unique()), default=sorted(reactors.technology_family.dropna().unique()))
    scenario_filter = st.sidebar.selectbox("Scenario", sorted(scenarios.scenario.dropna().unique()) if not scenarios.empty else ["Base"], index=0)
    capacity_factor = st.sidebar.slider("Capacity factor", 0.50, 0.95, 0.86, 0.01)
    price = st.sidebar.slider("Price per MWh", 20, 200, 75, 5)
    realization_adjustment = st.sidebar.slider("Project realization adjustment", 0.25, 1.25, 1.00, 0.05)

    r = reactors[reactors.country.isin(country_filter) & reactors.region.isin(region_filter) & reactors.status_group.isin(status_filter) & reactors.technology_family.isin(tech_filter)]
    p = pipeline[pipeline.country.isin(country_filter)] if not pipeline.empty else pipeline
    c = countries[countries.country.isin(country_filter)] if not countries.empty else countries

    pages = [
        "Executive Overview", "Global Nuclear Map", "Country Deep Dive", "Reactor Pipeline",
        "Technology Mix", "SMR / Gen IV / Thorium Watch", "Forecasting", "Project Risk Scoring",
        "Electricity Supply Scenarios", "Country Strategy Clustering", "NLP / Policy Intelligence",
        "Data Quality & Source Coverage", "Executive Report", "Power BI Export"
    ]
    page = st.sidebar.radio("Page", pages)

    if page == "Executive Overview":
        cols = st.columns(4)
        cols[0].metric("Operating reactors", int((r.status_group == "Operating").sum()))
        cols[1].metric("Operating capacity", f"{r.loc[r.status_group=='Operating','capacity_mwe'].sum()/1000:,.1f} GWe")
        cols[2].metric("Under construction", int((r.status_group == "Construction").sum()))
        cols[3].metric("Construction capacity", f"{r.loc[r.status_group=='Construction','capacity_mwe'].sum()/1000:,.1f} GWe")
        cols = st.columns(4)
        cols[0].metric("Planned capacity", f"{r.loc[r.status_group=='Planned','capacity_mwe'].sum()/1000:,.1f} GWe")
        cols[1].metric("Proposed capacity", f"{r.loc[r.status_group=='Proposed','capacity_mwe'].sum()/1000:,.1f} GWe")
        cols[2].metric("Countries with nuclear records", r.country.nunique())
        cols[3].metric("2050 scenario TWh", f"{scenarios[(scenarios.year==2050)&(scenarios.scenario==scenario_filter)].estimated_generation_twh.sum():,.0f}")
        left, right = st.columns([1.2, 1])
        with left:
            cap = r.groupby("country", as_index=False)["capacity_mwe"].sum().sort_values("capacity_mwe", ascending=False).head(12)
            st.plotly_chart(px.bar(cap, x="country", y="capacity_mwe", title="Capacity by Country", template="plotly_white"), use_container_width=True)
        with right:
            st.info("Generated insight: construction-stage projects and mature LWR technologies drive near-term capacity confidence. SMR and Gen IV concepts are best read as strategic signals until deployment history improves.")
            st.dataframe(p.sort_values("realization_probability", ascending=False).head(5), use_container_width=True)

    elif page == "Global Nuclear Map":
        st.plotly_chart(px.scatter_geo(r, lat="latitude", lon="longitude", size="capacity_mwe", color="status_group", hover_name="reactor_name", hover_data=["country","reactor_type_standardized","technology_family","source_name"], projection="natural earth", title="Global Reactor / Project Map", template="plotly_white"), use_container_width=True)
        st.dataframe(r, use_container_width=True)

    elif page == "Country Deep Dive":
        selected = st.selectbox("Select country", sorted(countries.country.dropna().unique()))
        cr = reactors[reactors.country == selected]
        cp = pipeline[pipeline.country == selected]
        st.subheader(selected)
        st.dataframe(countries[countries.country == selected], use_container_width=True)
        a, b = st.columns(2)
        a.plotly_chart(px.bar(cr.groupby("status_group", as_index=False)["capacity_mwe"].sum(), x="status_group", y="capacity_mwe", title="Fleet and Pipeline Status", template="plotly_white"), use_container_width=True)
        b.plotly_chart(px.bar(cr.groupby("technology_family", as_index=False)["capacity_mwe"].sum(), x="technology_family", y="capacity_mwe", title="Technology Mix", template="plotly_white"), use_container_width=True)
        st.dataframe(cp, use_container_width=True)

    elif page == "Reactor Pipeline":
        st.plotly_chart(px.bar(p.groupby("expected_operation_year", as_index=False)["capacity_mwe"].sum(), x="expected_operation_year", y="capacity_mwe", title="Expected Pipeline Additions", template="plotly_white"), use_container_width=True)
        st.plotly_chart(px.histogram(p, x="status_group", color="technology_family", title="Pipeline Funnel", template="plotly_white"), use_container_width=True)
        st.dataframe(p, use_container_width=True)

    elif page == "Technology Mix":
        a, b = st.columns(2)
        a.plotly_chart(px.pie(r, names="reactor_type_standardized", values="capacity_mwe", title="Fleet Reactor Type Mix"), use_container_width=True)
        b.plotly_chart(px.bar(taxonomy, x="reactor_type", y="maturity_score", color="technology_family", title="Technology Maturity", template="plotly_white"), use_container_width=True)
        st.dataframe(taxonomy, use_container_width=True)

    elif page == "SMR / Gen IV / Thorium Watch":
        adv = taxonomy[(taxonomy.smr_flag == True) | (taxonomy.geniv_flag == True) | (taxonomy.thorium_potential_flag == True)]
        st.plotly_chart(px.scatter(adv, x="known_operating_units", y="maturity_score", size="known_under_construction_units", color="technology_family", hover_name="reactor_type", title="Maturity vs Deployment Reality", template="plotly_white"), use_container_width=True)
        st.warning("Advanced technologies are scored as maturity and scenario indicators, not deterministic forecast targets.")
        st.dataframe(adv, use_container_width=True)

    elif page == "Forecasting":
        st.plotly_chart(px.bar(forecasts, x="country", y="forecast_capacity_2035_mwe", color="region", title="Forecast Capacity by Country", template="plotly_white"), use_container_width=True)
        st.dataframe(metrics, use_container_width=True)
        st.download_button("Download predictions", forecasts.to_csv(index=False), "capacity_forecasts.csv")

    elif page == "Project Risk Scoring":
        st.plotly_chart(px.scatter(risk, x="project_maturity_score", y="delay_risk_score", size="capacity_mwe", color="risk_level", hover_name="reactor_name", title="Project Risk Matrix", template="plotly_white"), use_container_width=True)
        st.dataframe(risk.sort_values("delay_risk_score", ascending=False), use_container_width=True)

    elif page == "Electricity Supply Scenarios":
        s = scenarios[scenarios.scenario == scenario_filter].copy()
        s["estimated_generation_twh_adjusted"] = s.capacity_gwe * capacity_factor * 8.76 * realization_adjustment
        s["estimated_market_value_usd"] = s.estimated_generation_twh_adjusted * 1_000_000 * price
        st.metric("Estimated scenario generation", f"{s.estimated_generation_twh_adjusted.sum():,.0f} TWh/year")
        st.metric("Estimated market value proxy", f"${s.estimated_market_value_usd.sum()/1e9:,.1f}B")
        st.plotly_chart(px.line(s.groupby("year", as_index=False)["estimated_generation_twh_adjusted"].sum(), x="year", y="estimated_generation_twh_adjusted", title="Scenario Generation Sensitivity", template="plotly_white"), use_container_width=True)
        st.dataframe(s, use_container_width=True)

    elif page == "Country Strategy Clustering":
        st.plotly_chart(px.scatter(clusters, x="pca_x", y="pca_y", color="cluster_name", hover_name="country", title="Country Nuclear Strategy Clusters", template="plotly_white"), use_container_width=True)
        st.dataframe(clusters, use_container_width=True)

    elif page == "NLP / Policy Intelligence":
        if docs.empty:
            st.warning("NLP outputs missing.")
        else:
            st.plotly_chart(px.bar(docs, x="country", y="policy_support_signal", color="detected_topics", title="Policy Signal Score", template="plotly_white"), use_container_width=True)
            st.dataframe(docs, use_container_width=True)

    elif page == "Data Quality & Source Coverage":
        st.plotly_chart(px.imshow(reactors.isna(), title="Missingness Heatmap", aspect="auto"), use_container_width=True)
        st.dataframe(load_csv(config.PROCESSED / "data_sources.csv"), use_container_width=True)
        st.warning("Fallback sample data is labeled sample-only. Replace or augment it with official/manual source exports for production use.")

    elif page == "Executive Report":
        report_path = config.REPORTS / "global_nuclear_buildout_report.md"
        text = report_path.read_text(encoding="utf-8") if report_path.exists() else "Run the pipeline to generate the report."
        st.markdown(text)
        st.download_button("Download markdown report", text, "global_nuclear_buildout_report.md")

    elif page == "Power BI Export":
        st.write("Power BI CSV exports live in `data/powerbi/`.")
        st.dataframe(pd.DataFrame({"file": sorted([p.name for p in config.POWERBI.glob("*.csv")])}), use_container_width=True)
        st.markdown(Path(config.DOCS / "powerbi_guide.md").read_text(encoding="utf-8") if (config.DOCS / "powerbi_guide.md").exists() else "")
    """)
    for page in ["executive_overview.py","global_map.py","country_deep_dive.py","reactor_pipeline.py","technology_mix.py","forecasting.py","project_risk.py","smr_geniv_watch.py","electricity_scenarios.py","nlp_policy_intelligence.py","data_quality.py","executive_report.py"]:
        write(f"src/dashboard/pages/{page}", "# Page logic is implemented in src/dashboard/app.py for this portable portfolio build.\n")
    write("src/dashboard/assets/custom_style.css", "/* Additional dashboard CSS can be added here. */\n")

    write("spark/pyspark_etl.py", """
    from __future__ import annotations
    from pathlib import Path

    def main() -> None:
        try:
            from pyspark.sql import SparkSession
            import pyspark.sql.functions as F
        except Exception as exc:
            print(f"PySpark is not installed. Install pyspark to run scalable ETL. Reason: {exc}")
            return
        root = Path(__file__).resolve().parents[1]
        spark = SparkSession.builder.appName("global-nuclear-buildout-intelligence").getOrCreate()
        reactors = spark.read.option("header", True).option("inferSchema", True).csv(str(root / "data/processed/reactors_master.csv"))
        out = reactors.groupBy("country","technology_family","status_group").agg(F.sum("capacity_mwe").alias("capacity_mwe"), F.count("*").alias("reactor_count"))
        target = root / "data/analytics/spark_capacity_by_country_technology"
        out.write.mode("overwrite").parquet(str(target))
        print(f"Wrote {target}")
        spark.stop()

    if __name__ == "__main__":
        main()
    """)
    write("spark/databricks_notebook_template.py", '''
    # Databricks Notebook Template: Global Nuclear Buildout Intelligence
    # COMMAND ----------
    # Load raw sources from cloud storage or mounted volumes.
    # COMMAND ----------
    # Standardize reactor status, dates, technology taxonomy and source confidence.
    # COMMAND ----------
    # Build country features, pipeline features and scenario tables.
    # COMMAND ----------
    # Write Delta/Parquet tables for reactors, countries, technologies, pipeline, scenarios and NLP.
    # COMMAND ----------
    # This dataset may not be huge locally, but the architecture is Databricks-ready and could scale
    # to many years of snapshots, policy documents, market data, project updates and energy system data.
    ''')
    write("spark/README_databricks.md", """
    # Databricks Readiness

    The local CSV pipeline is intentionally mirrored by `pyspark_etl.py`. A production client version would land raw snapshots in cloud storage, standardize them with Spark, write Delta tables, orchestrate refresh jobs, register models, and serve Power BI or Streamlit from curated tables.
    """)

    write("run_pipeline.py", """
    from __future__ import annotations
    import sys
    from pathlib import Path

    ROOT = Path(__file__).resolve().parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    from src.utils.paths import ensure_dirs
    from src.data.source_registry import register_sources
    from src.data.manual_ingestion_templates import create_manual_templates
    from src.data.sample_data import create_dirty_sample_data
    from src.data.ingest_owid_ember import ingest_owid
    from src.data.ingest_world_bank import ingest_world_bank
    from src.data.integrate_sources import integrate_all
    from src.data.data_quality_checks import run_data_quality_checks
    from src.nlp.policy_signal_scoring import run_nlp_pipeline
    from src.eda.eda_report_generator import generate_eda_outputs
    from src.models.capacity_forecasting_xgboost import train_capacity_forecaster
    from src.models.capacity_forecasting_statsmodels import run_statsmodels_global_forecast
    from src.models.project_realization_classifier import train_project_realization_models
    from src.models.technology_maturity_score import score_technology_maturity
    from src.models.country_clustering import cluster_countries
    from src.models.model_evaluation import write_model_metrics_table
    from src.sql.build_database import build_sqlite_database
    from src.sql.run_queries import run_sql_queries
    from src.sql.export_powerbi_tables import export_powerbi_tables
    from src.reports.generate_executive_report import generate_executive_report
    from src.reports.generate_model_card import generate_model_card
    from src.reports.generate_interview_brief import generate_interview_brief

    def step(i: int, msg: str) -> None:
        print(f"[{i}/21] {msg}", flush=True)

    def main() -> None:
        step(1, "Initializing folders...")
        ensure_dirs()
        step(2, "Registering data sources...")
        register_sources()
        step(3, "Ingesting available data sources...")
        try:
            ingest_owid()
            ingest_world_bank()
        except Exception as exc:
            print(f"Warning: optional download failed and pipeline will continue: {exc}")
        step(4, "Generating manual ingestion templates...")
        create_manual_templates()
        create_dirty_sample_data()
        step(5, "Cleaning source datasets...")
        step(6, "Integrating reactor master table...")
        reactors, countries, pipeline, taxonomy, scenarios = integrate_all()
        step(7, "Integrating country profile table...")
        step(8, "Building technology taxonomy...")
        step(9, "Running data quality checks...")
        run_data_quality_checks(reactors, countries)
        step(10, "Running full EDA...")
        docs, topics = run_nlp_pipeline()
        generate_eda_outputs(reactors, countries, pipeline, taxonomy, scenarios, topics)
        step(11, "Building forecasting features...")
        step(12, "Training forecasting models...")
        forecasts, forecast_metrics = train_capacity_forecaster(countries)
        run_statsmodels_global_forecast(reactors)
        step(13, "Building project risk scoring...")
        risk, risk_metrics = train_project_realization_models(pipeline)
        step(14, "Building technology maturity scoring...")
        score_technology_maturity(taxonomy)
        step(15, "Running country clustering...")
        cluster_countries(countries)
        step(16, "Running electricity supply scenarios...")
        # Scenario table was generated during integration and exported to predictions.
        step(17, "Running NLP pipeline...")
        # NLP was run before EDA so figures can use topic outputs.
        step(18, "Building SQLite database...")
        write_model_metrics_table(forecast_metrics, risk_metrics)
        build_sqlite_database()
        run_sql_queries()
        step(19, "Exporting Power BI tables...")
        export_powerbi_tables()
        step(20, "Generating executive report...")
        generate_executive_report()
        generate_model_card()
        step(21, "Generating interview brief...")
        generate_interview_brief()
        print("Pipeline complete. Run: streamlit run src/dashboard/app.py")

    if __name__ == "__main__":
        main()
    """)

    write("run_dashboard.py", """
    from __future__ import annotations
    import subprocess
    import sys

    if __name__ == "__main__":
        raise SystemExit(subprocess.call([sys.executable, "-m", "streamlit", "run", "src/dashboard/app.py"]))
    """)

    write("docs/DECISIONS_REQUIRED.md", """
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
    """)

    write("docs/data_sources_inventory.md", """
    # Data Sources Inventory

    The project registers every source in `data/processed/data_sources.csv` with source name, type, URL/reference, date accessed, fields used, limitations and reliability rating.

    Key sources: IAEA PRIS, IAEA RDS-1, IAEA ARIS, IAEA SMR Catalogue, World Nuclear Association, Global Energy Monitor Global Nuclear Power Tracker, Our World in Data Energy, World Bank WDI, EIA International, and labeled dirty sample data.

    Official sources are preferred where available. Where a public source is not reliably machine-downloadable, the repository provides a manual ingestion template and expected schema.
    """)
    write("docs/data_dictionary.md", """
    # Data Dictionary

    Main processed tables:
    - `reactors_master.csv`: standardized reactor/unit table.
    - `country_nuclear_profile.csv`: country energy, economy, fleet and policy indicators.
    - `reactor_pipeline.csv`: projects, maturity, risk and realization scoring.
    - `technology_taxonomy.csv`: reactor technology classification and maturity attributes.
    - `nuclear_capacity_scenarios.csv`: 2030/2040/2050 scenario outputs.
    - `nlp_policy_documents.csv`: policy text, topics and signal scores.
    - `model_metrics.csv`: model evaluation and caveats.
    """)
    write("docs/source_limitations.md", """
    # Source Limitations

    Public nuclear data is fragmented across official databases, PDFs, industry pages, trackers and country-level documents. Official data generally has high reliability but may be difficult to bulk-download. Industry and NGO sources can be more accessible but may use different status definitions.

    Planned and proposed projects are uncertain. Expected operation dates can shift because of financing, licensing, supply chain, construction, policy or grid factors.

    SMR, Gen IV, molten salt, thorium and fast reactor concepts should be interpreted as maturity and strategic signals unless deployment data supports stronger claims. Scenario modelling is more appropriate than deterministic prediction for these technologies.
    """)
    write("docs/methodology.md", """
    # Methodology

    The pipeline standardizes reactor status, reactor types, technology families, country context, pipeline maturity and technology maturity. Capacity scenarios convert GWe into TWh using capacity factor assumptions.

    Project risk scoring combines project stage, technology maturity, country experience, GDP context and size complexity. Realization probability is a decision-support score, not an official probability.

    Forecasting uses a scenario-derived target in the portfolio build. In production, the same model structure should be trained on historical project snapshots and actual completion outcomes.

    NLP uses NLTK-compatible tokenization/stopwords, keyword extraction and rule-based topic tagging for nuclear policy and technology signals.
    """)
    write("docs/architecture.md", """
    # Architecture

    Raw/manual sources -> cleaning and standardization -> processed analytics tables -> EDA, ML, NLP, scenarios -> SQLite, Power BI exports, Streamlit dashboard and executive reports.

    A production version can use Databricks, Delta Lake, cloud object storage, scheduled ingestion, a model registry, SQL warehouse, Power BI Service and an internal Streamlit/web application.
    """)
    write("docs/dashboard_guide.md", """
    # Dashboard Guide

    Run `streamlit run src/dashboard/app.py`. The dashboard reads processed outputs only and does not train models live. Use the sidebar to filter by country, region, status, technology, scenario, capacity factor and price assumptions.
    """)
    write("docs/powerbi_guide.md", """
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
    """)

    write("powerbi/README_powerbi.md", "# Power BI\n\nRun `python run_pipeline.py`, then import CSVs from `data/powerbi/` into Power BI Desktop.\n")
    write("powerbi/nuclear_buildout_powerbi_schema.md", "# Power BI Schema\n\nRecommended star schema: fact tables around country, region, technology and date dimensions.\n")

    write("README.md", """
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
    """)

    for test_file, content in {
        "test_data_ingestion.py": "from src.data.source_registry import register_sources\n\ndef test_source_registry():\n    assert not register_sources().empty\n",
        "test_data_quality.py": "import pandas as pd\nfrom src.data.data_quality_checks import run_data_quality_checks\n\ndef test_quality_smoke():\n    r=pd.DataFrame({'reactor_id':['a'],'country':['X'],'source_name':['s'],'source_confidence':[.5]})\n    c=pd.DataFrame({'country':['X']})\n    assert run_data_quality_checks(r,c)['reactor_rows']==1\n",
        "test_feature_engineering.py": "from src.features.reactor_features import add_reactor_feature_flags\nimport pandas as pd\n\ndef test_flags():\n    df=pd.DataFrame({'reactor_type_standardized':['MSR'],'technology_family':['Molten Salt Reactor']})\n    assert add_reactor_feature_flags(df).loc[0,'molten_salt_flag']\n",
        "test_models.py": "def test_model_imports():\n    import src.models.country_clustering\n",
        "test_scenarios.py": "from src.models.electricity_supply_scenarios import estimate_generation_twh\n\ndef test_generation_formula():\n    assert round(estimate_generation_twh(1, .9), 2) == 7.88\n",
        "test_sql_exports.py": "def test_sql_imports():\n    import src.sql.build_database\n",
    }.items():
        write(f"tests/{test_file}", content)

    print(f"Scaffold complete: {ROOT}")


if __name__ == "__main__":
    main()
