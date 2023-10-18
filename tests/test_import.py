"""Test geotech-pandas."""

import geotech_pandas


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(geotech_pandas.__name__, str)
