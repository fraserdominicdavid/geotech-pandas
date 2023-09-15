import pandas as pd
import pandas._testing as tm

from geotech_pandas.point import PointDataFrameAccessor

base_df = pd.DataFrame(
    {
        "PointID": ["BH-1", "BH-1", "BH-2", "BH-2"],
        "Bottom": [0.0, 1.0, 0.0, 1.0],
    }
)


def test_groups():
    """Test if groups property returns a `DataFrameGroupBy` object."""
    df = PointDataFrameAccessor(base_df)
    g = df.groups
    assert len(base_df["PointID"].unique()) == len(g)


def test_get_group():
    """Test if `get_group` returns the correct `DataFrame` object."""
    df = PointDataFrameAccessor(base_df)
    for point_id in base_df["PointID"].to_list():
        tm.assert_frame_equal(base_df[base_df["PointID"] == point_id], df.get_group(point_id))
