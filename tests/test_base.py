"""Test base class methods."""

from contextlib import nullcontext as does_not_raise

import pandas as pd
import pandas._testing as tm
import pytest

import geotech_pandas  # noqa: F401

base_df = pd.DataFrame(
    {
        "point_id": ["BH-1", "BH-1", "BH-2", "BH-2"],
        "bottom": [0.0, 1.0, 0.0, 1.0],
    }
)


def test_obj():
    """Test if dataframe is stored in ``_obj``."""
    df = base_df
    tm.assert_frame_equal(base_df, df.geotech._obj)


@pytest.mark.parametrize(
    ("df", "columns", "error", "error_message"),
    [
        (
            base_df[["point_id"]].copy(),
            None,
            pytest.raises(AttributeError),
            "The dataframe must have: bottom column.",
        ),
        (
            base_df[["point_id"]].copy(),
            ["point_id", "top", "bottom"],
            pytest.raises(AttributeError),
            "The dataframe must have: top, bottom columns.",
        ),
        (
            base_df,
            ["point_id", "top", "bottom"],
            pytest.raises(AttributeError),
            "The dataframe must have: top column.",
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
        df.geotech._validate_columns(columns)
        assert error_message is None or error_message in str(e)


@pytest.mark.parametrize(
    ("df", "error", "error_message"),
    [
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 2.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(AttributeError),
            "Elements in the bottom column must be monotonically increasing for: BH-1.",
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 2.0, 0.0, 1.0],
                }
            ),
            does_not_raise(),
            None,
        ),
    ],
)
def test_validate_monotony(df, error, error_message):
    """Test if the ``bottom`` of each ``point_id`` group is monotonically increasing."""
    with error as e:
        df.geotech._validate_monotony()
        assert error_message is None or error_message in str(e)


@pytest.mark.parametrize(
    ("df", "error", "error_message"),
    [
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(AttributeError),
            "The dataframe contains duplicate point_id and bottom: BH-1.",
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 2.0, 0.0, 1.0],
                }
            ),
            does_not_raise(),
            None,
        ),
    ],
)
def test_validate_duplicates(df, error, error_message):
    """Test df for duplicate value pairs in the ``point_id`` and ``bottom`` columns."""
    with error as e:
        df.geotech._validate_duplicates()
        assert error_message is None or error_message in str(e)


@pytest.mark.parametrize(
    ("df", "error", "error_message"),
    [
        (
            base_df[["point_id"]].copy(),
            pytest.raises(AttributeError),
            "The dataframe must have: bottom column.",
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 2.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(AttributeError),
            "Elements in the bottom column must be monotonically increasing for: BH-1.",
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(AttributeError),
            "The dataframe contains duplicate point_id and bottom: BH-1.",
        ),
        (
            base_df,
            does_not_raise(),
            None,
        ),
    ],
)
def test_validators(df, error, error_message):
    """Test if validators are triggered for wrong dataframe configurations."""
    with error as e:
        df.geotech  # noqa: B018
        assert error_message is None or error_message in str(e)
