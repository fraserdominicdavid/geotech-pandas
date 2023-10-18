"""Test ``layer`` subaccessor methods."""
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
    isinstance(pd.DataFrame.geotech.layer, geotech_pandas.layer.LayerDataFrameAccessor)


def test_get_top():
    """Test if ``get_top`` returns the correct shifted ``bottom`` depths."""
    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
        }
    )
    tm.assert_series_equal(df.geotech.layer.get_top(), pd.Series([0.0, 1.0, 0.0, 3.0], name="top"))


def test_get_center():
    """Test if ``get_center`` returns the correct values."""
    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
        }
    )
    tm.assert_series_equal(
        df.geotech.layer.get_center(), pd.Series([0.5, 1.5, 1.5, 3.5], name="center")
    )


def test_get_thickness():
    """Test if ``get_thickness`` returns the correct values."""
    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
        }
    )
    tm.assert_series_equal(
        df.geotech.layer.get_thickness(), pd.Series([1.0, 1.0, 3.0, 1.0], name="thickness")
    )


def test_split_at_depth_numeric():
    """Test if ``split_at_depth`` with ``depth`` as a numeric value will return the correct
    result.
    """  # noqa: D205
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
    result = result.geotech.layer.split_at(depth=0.5)
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_series():
    """Test if ``split_at_depth`` with ``depth`` as a ``Series`` will return the correct result."""
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
    result = result.geotech.layer.split_at(depth=pd.Series([0.5, 0.5, 1.5, 1.5]))
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_str():
    """Test if ``split_at_depth`` with ``depth`` as a ``str`` value will return the correct
    result.
    """  # noqa: D205
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
    result = result.geotech.layer.split_at(depth="water_level")
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_no_split():
    """Test if ``split_at_depth`` where no splitting should happen will return the correct
    result.
    """  # noqa: D205
    expected = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
            "bottom": [1.0, 2.0, 3.0, 4.0],
            "top": [0.0, 1.0, 0.0, 3.0],
            "thickness": [1.0, 1.0, 3.0, 1.0],
        }
    )
    result = expected.copy()
    result = result.geotech.layer.split_at(0)
    tm.assert_frame_equal(result, expected)


def test_split_at_depth_no_index_reset():
    """Test if ``split_at_depth`` with ``reset_index`` set to ``True`` will return the correct
    result.

    The expected result should have the added layers take the original index of the split layers.
    """  # noqa: D205
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
    result = result.geotech.layer.split_at(depth=0.5, reset_index=False)
    tm.assert_frame_equal(result, expected)
