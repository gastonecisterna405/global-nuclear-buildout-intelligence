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
