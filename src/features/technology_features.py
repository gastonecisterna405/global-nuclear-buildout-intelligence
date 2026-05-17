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
