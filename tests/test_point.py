import pandas as pd
import pandas._testing as tm

from geotech_pandas.point import PointDataFrameAccessor

base_df = pd.DataFrame(
    {
        "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
        "bottom": [0.0, 1.0, 0.0, 1.0],
    }
)


def test_groups():
    """Test if groups property returns a `DataFrameGroupBy` object."""
    df = PointDataFrameAccessor(base_df)
    g = df.groups
    assert len(base_df["point_id"].unique()) == len(g)


def test_get_group():
    """Test if `get_group` returns the correct `DataFrame` object."""
    df = PointDataFrameAccessor(base_df)
    for point_id in base_df["point_id"].to_list():
        tm.assert_frame_equal(base_df[base_df["point_id"] == point_id], df.get_group(point_id))


def test_get_top():
    """Test if `get_top` returns correct shifted ``bottom`` depths."""
    df = PointDataFrameAccessor(
        pd.DataFrame(
            {
                "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
                "bottom": [1.0, 2.0, 3.0, 4.0],
            }
        )
    )
    tm.assert_series_equal(df.get_top(), pd.Series([0.0, 1.0, 0.0, 3.0], name="top"))


def test_get_center():
    """Test if `get_center` returns correct depth values."""
    df = PointDataFrameAccessor(
        pd.DataFrame(
            {
                "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
                "bottom": [1.0, 2.0, 3.0, 4.0],
                "top": [0.0, 1.0, 0.0, 3.0],
            }
        )
    )
    tm.assert_series_equal(df.get_center(), pd.Series([0.5, 1.5, 1.5, 3.5], name="center"))


def test_get_thickness():
    """Test if `get_thickness` returns correct values."""
    df = PointDataFrameAccessor(
        pd.DataFrame(
            {
                "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
                "bottom": [1.0, 2.0, 3.0, 4.0],
                "top": [0.0, 1.0, 0.0, 3.0],
            }
        )
    )
    tm.assert_series_equal(df.get_thickness(), pd.Series([1.0, 1.0, 3.0, 1.0], name="thickness"))


def test_split_at_depth_numeric():
    """Test if `split_at_depth` with `depth` as a numeric value will return the correct result."""
    expected = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2", "BH-2"],
            "bottom": [0.5, 1.0, 2.0, 0.5, 3.0, 4.0],
            "top": [0.0, 0.5, 1.0, 0.0, 0.5, 3.0],
            "thickness": [1.0, 1.0, 1.0, 3.0, 3.0, 1.0],
        }
    )
    result = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
            "thickness": [1.0, 1.0, 3.0, 1.0],
        }
    )
    result = PointDataFrameAccessor(result).split_at_depth(depth=0.5)
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_series():
    """Test if `split_at_depth` with `depth` as a series will return the correct result."""
    expected = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2", "BH-2"],
            "bottom": [0.5, 1.0, 2.0, 1.5, 3.0, 4.0],
            "top": [0.0, 0.5, 1.0, 0.0, 1.5, 3.0],
        }
    )
    result = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
        }
    )
    result = PointDataFrameAccessor(result).split_at_depth(depth=pd.Series([0.5, 0.5, 1.5, 1.5]))
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_str():
    """Test if `split_at_depth` with `depth` as a str value will return the correct result."""
    expected = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2", "BH-2"],
            "water_level": [0.5, 0.5, 0.5, 1.5, 1.5, 1.5],
            "bottom": [0.5, 1.0, 2.0, 1.5, 3.0, 4.0],
            "top": [0.0, 0.5, 1.0, 0.0, 1.5, 3.0],
        }
    )
    result = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "water_level": [0.5, 0.5, 1.5, 1.5],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
        }
    )
    result = PointDataFrameAccessor(result).split_at_depth(depth="water_level")
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_no_split():
    """Test if `split_at_depth` where no splitting should happen will return the correct result."""
    expected = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
            "thickness": [1.0, 1.0, 3.0, 1.0],
        }
    )
    result = expected.copy()
    result = PointDataFrameAccessor(result).split_at_depth(0)
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_no_index_reset():
    """Test if `split_at_depth` with `reset_index` set to `True` will return the correct result.

    The expected result should have the added layers take the original index of the split layers.
    """
    expected = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2", "BH-2"],
            "bottom": [0.5, 1.0, 2.0, 0.5, 3.0, 4.0],
            "top": [0.0, 0.5, 1.0, 0.0, 0.5, 3.0],
        },
        index=[0, 0, 1, 2, 2, 3],
    )
    result = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
        }
    )
    result = PointDataFrameAccessor(result).split_at_depth(depth=0.5, reset_index=False)
    tm.assert_frame_equal(result, expected)
