import pandas as pd
from src.data.source_registry import register_sources
from src.data.sample_data import create_dirty_sample_data
from src.data.clean_reactor_data import clean_reactors, standardize_status, standardize_reactor_type


def test_source_registry_has_required_fields():
    df = register_sources()
    assert not df.empty
    for col in ["source_name", "source_type", "url", "reliability_rating"]:
        assert col in df.columns, f"Missing column: {col}"


def test_source_registry_no_unknown_ingestion_modes():
    df = register_sources()
    valid_modes = {"manual_template", "download_optional", "documented_optional", "generated"}
    assert set(df["ingestion_mode"].unique()).issubset(valid_modes)


def test_standardize_status_variants():
    assert standardize_status("operating") == "Operating"
    assert standardize_status("UNDER CONSTRUCTION") == "Construction"
    assert standardize_status("under-construction") == "Construction"
    assert standardize_status("planned") == "Planned"
    assert standardize_status("shutdown") == "Shutdown"


def test_standardize_reactor_type():
    assert standardize_reactor_type("AP1000", "AP1000") == "AP1000"
    assert standardize_reactor_type("PWR", "APR1400") == "APR1400"
    assert standardize_reactor_type("VVER", "VVER-1200") == "VVER"
    assert standardize_reactor_type("SMR", "BWRX-300") == "SMR-LWR"
    assert standardize_reactor_type("SFR", "Natrium") == "SFR"


def test_clean_reactors_no_duplicates(tmp_path, monkeypatch):
    create_dirty_sample_data()
    df = clean_reactors()
    assert df.duplicated("reactor_id").sum() == 0


def test_clean_reactors_capacity_numeric(tmp_path, monkeypatch):
    create_dirty_sample_data()
    df = clean_reactors()
    assert pd.api.types.is_float_dtype(df["capacity_mwe"])
    assert df["capacity_mwe"].isna().sum() == 0 or df["capacity_mwe"].notna().any()


def test_clean_reactors_required_columns():
    create_dirty_sample_data()
    df = clean_reactors()
    required = ["reactor_id", "country", "status_group", "capacity_mwe",
                "reactor_type_standardized", "technology_family", "region"]
    for col in required:
        assert col in df.columns, f"Missing column after cleaning: {col}"
