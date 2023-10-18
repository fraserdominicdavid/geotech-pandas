"""Test ``point`` subaccessor methods."""
import pandas as pd
import pandas._testing as tm

import geotech_pandas

base_df = pd.DataFrame(
    {
        "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
        "bottom": [0.0, 1.0, 0.0, 1.0],
    }
)


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.point, geotech_pandas.point.PointDataFrameAccessor)


def test_groups():
    """Test if groups property returns a ``DataFrameGroupBy`` object."""
    df = base_df
    g = df.geotech.point.groups
    assert len(base_df["point_id"].unique()) == len(g)


def test_get_group():
    """Test if ``get_group`` returns the correct ``DataFrame`` object."""
    df = base_df
    for point_id in base_df["point_id"].to_list():
        tm.assert_frame_equal(
            base_df[base_df["point_id"] == point_id], df.geotech.point.get_group(point_id)
        )
