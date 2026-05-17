from src.data.source_registry import register_sources

def test_source_registry():
    assert not register_sources().empty
