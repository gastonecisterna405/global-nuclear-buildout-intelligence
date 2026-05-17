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
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        written.append(str(path))
    return written
