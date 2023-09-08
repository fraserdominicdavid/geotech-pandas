"""Test base class methods."""

from contextlib import nullcontext as does_not_raise

import pandas as pd
import pandas._testing as tm
import pytest

from geotech_pandas.base import GeotechPandasBase

base_df = pd.DataFrame(
    {
        "PointID": ["BH-1", "BH-1", "BH-2", "BH-2"],
        "Bottom": [0.0, 1.0, 0.0, 1.0],
    }
)


def test_obj():
    """Test if dataframe is stored in ``_obj``."""
    gpdf = GeotechPandasBase(base_df)
    tm.assert_frame_equal(base_df, gpdf._obj)


@pytest.mark.parametrize(
    ("df", "columns", "error", "error_message"),
    [
        (
            base_df[["PointID"]].copy(),
            None,
            pytest.raises(AttributeError),
            "The dataframe must have: Bottom column.",
        ),
        (
            base_df[["PointID"]].copy(),
            ["PointID", "Top", "Bottom"],
            pytest.raises(AttributeError),
            "The dataframe must have: Top, Bottom columns.",
        ),
        (
            base_df,
            ["PointID", "Top", "Bottom"],
            pytest.raises(AttributeError),
            "The dataframe must have: Top column.",
        ),
        (
            base_df,
            None,
            does_not_raise(),
            None,
        ),
    ],
)
def test_validate_columns(df, columns, error, error_message):
    """Test if columns are in df else raise error with error_message."""
    with error as e:
        GeotechPandasBase.validate_columns(df, columns)
        assert error_message is None or error_message in str(e)


@pytest.mark.parametrize(
    ("df", "error", "error_message"),
    [
        (
            pd.DataFrame(
                {
                    "PointID": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "Bottom": [0.0, 2.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(AttributeError),
            "Elements in the Bottom column must be monotonically increasing for: BH-1.",
        ),
        (
            pd.DataFrame(
                {
                    "PointID": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "Bottom": [0.0, 1.0, 2.0, 0.0, 1.0],
                }
            ),
            does_not_raise(),
            None,
        ),
    ],
)
def test_validate_monotony(df, error, error_message):
    """Test if the ``Bottom`` of each ``PointID`` group is monotonically increasing."""
    with error as e:
        GeotechPandasBase.validate_monotony(df)
        assert error_message is None or error_message in str(e)
