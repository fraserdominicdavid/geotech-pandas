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
    """Test if the ``DataFrame`` is stored in ``_obj``."""
    df = base_df
    tm.assert_frame_equal(base_df, df.geotech._obj)


@pytest.mark.parametrize(
    ("df", "columns", "error"),
    [
        (
            base_df[["point_id"]].copy(),
            None,
            pytest.raises(
                AttributeError,
                match="The DataFrame must have: bottom column.",
            ),
        ),
        (
            base_df,
            ["top", "soil_type"],
            pytest.raises(
                AttributeError,
                match="The DataFrame must have: top, soil_type columns.",
            ),
        ),
        (
            base_df,
            ["top"],
            pytest.raises(
                AttributeError,
                match="The DataFrame must have: top column.",
            ),
        ),
        (
            base_df,
            None,
            does_not_raise(),
        ),
    ],
)
def test_validate_columns(df, columns, error):
    """Test if ``columns`` are in ``df`` else raise ``error``."""
    with error:
        df.geotech._validate_columns(columns)


@pytest.mark.parametrize(
    ("df", "error"),
    [
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 2.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(
                AttributeError,
                match="Elements in the bottom column must be monotonically increasing for: BH-1.",
            ),
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 2.0, 0.0, 1.0],
                }
            ),
            does_not_raise(),
        ),
    ],
)
def test_validate_monotony(df, error):
    """Test if the ``bottom`` of each ``point_id`` group is monotonically increasing."""
    with error:
        df.geotech._validate_monotony()


@pytest.mark.parametrize(
    ("df", "error"),
    [
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(
                AttributeError,
                match="The DataFrame contains duplicate point_id and bottom: BH-1.",
            ),
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 2.0, 0.0, 1.0],
                }
            ),
            does_not_raise(),
        ),
    ],
)
def test_validate_duplicates(df, error):
    """Test ``DataFrame`` for duplicate value pairs in the ``point_id`` and ``bottom`` columns."""
    with error:
        df.geotech._validate_duplicates()


@pytest.mark.parametrize(
    ("df", "error"),
    [
        (
            base_df[["point_id"]].copy(),
            pytest.raises(
                AttributeError,
                match="The DataFrame must have: bottom column.",
            ),
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 2.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(
                AttributeError,
                match="Elements in the bottom column must be monotonically increasing for: BH-1.",
            ),
        ),
        (
            pd.DataFrame(
                {
                    "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
                    "bottom": [0.0, 1.0, 1.0, 0.0, 1.0],
                }
            ),
            pytest.raises(
                AttributeError,
                match="The DataFrame contains duplicate point_id and bottom: BH-1.",
            ),
        ),
        (
            base_df,
            does_not_raise(),
        ),
    ],
)
def test_validators(df, error):
    """Test if validators are triggered for wrong ``DataFrame`` configurations."""
    with error:
        df.geotech  # noqa: B018
