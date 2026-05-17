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
