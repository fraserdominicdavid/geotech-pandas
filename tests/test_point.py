import pandas as pd

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
