"""Test ``point`` subaccessor methods."""

import pandas as pd
import pandas._testing as tm
import pytest

from geotech_pandas.point import PointDataFrameAccessor


@pytest.fixture
def df() -> pd.DataFrame:
    """Return common DataFrame for testing methods that return Series objects."""
    return pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [0.0, 1.0, 0.0, 1.0],
        }
    )


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.point, PointDataFrameAccessor)


def test_get_ids(df):
    """Test if ``ids`` property returns correct list."""
    assert df.geotech.point.ids == ["BH-1", "BH-2"]


def test_groups(df):
    """Test if groups property returns a ``DataFrameGroupBy`` object."""
    assert len(df["point_id"].unique()) == len(df.geotech.point.groups)


def test_get_group(df):
    """Test if ``get_group`` returns the correct ``DataFrame`` object."""
    for point_id in df["point_id"].to_list():
        tm.assert_frame_equal(df[df["point_id"] == point_id], df.geotech.point.get_group(point_id))
