import pandas as pd
from src.data.data_quality_checks import run_data_quality_checks


def _make_reactors(**kwargs):
    base = {
        "reactor_id": ["A", "B"],
        "country": ["X", "Y"],
        "source_name": ["s", "s"],
        "source_confidence": [0.8, 0.5],
    }
    base.update(kwargs)
    return pd.DataFrame(base)


def test_quality_smoke():
    r = _make_reactors()
    c = pd.DataFrame({"country": ["X", "Y"]})
    result = run_data_quality_checks(r, c)
    assert result["reactor_rows"] == 2
    assert result["country_rows"] == 2


def test_duplicate_detection():
    r = _make_reactors(reactor_id=["A", "A"])
    result = run_data_quality_checks(r, pd.DataFrame({"country": ["X"]}))
    assert result["duplicate_reactor_ids"] == 1


def test_missing_fraction_range():
    r = _make_reactors(source_confidence=[None, 0.5])
    result = run_data_quality_checks(r, pd.DataFrame({"country": ["X"]}))
    frac = result["missing_fraction_by_field"].get("source_confidence", 0)
    assert 0.0 <= frac <= 1.0
