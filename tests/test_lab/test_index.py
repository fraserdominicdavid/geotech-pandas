"""Test ``index`` subaccessor methods."""

from functools import reduce

import pandas as pd
import pandas._testing as tm
import pytest

from geotech_pandas.lab import IndexDataFrameAccessor


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.lab.index, IndexDataFrameAccessor)


@pytest.fixture
def df() -> pd.DataFrame:
    """Return common dataframe for testing methods."""
    return pd.DataFrame(
        {
            "point_id": ["bh-1", "bh-2", "bh-3", "bh-4", "None"],
            "bottom": [1, 1, 1, 1, 1],
            "moisture_content_mass_moist": [236.44, 154.40, 164.68, None, None],
            "moisture_content_mass_dry": [174.40, 120.05, 134.31, None, None],
            "moisture_content_mass_container": [22.20, 18.66, 20.27, None, None],
            "moisture_content": [40.76, 33.88, 26.63, None, None],
            "liquid_limit_1_drops": [23, 22, 17, 21, None],
            "liquid_limit_2_drops": [28, 27, 25, 29, None],
            "liquid_limit_3_drops": [33, 32, 34, 32, None],
            "liquid_limit_1_moisture_content": [48.1, 46.5, 42.4, 23.3, None],
            "liquid_limit_2_moisture_content": [46.7, 45.6, 41.5, 24.3, None],
            "liquid_limit_3_moisture_content": [46.1, 43.9, 40.9, 25.1, None],
            "liquid_limit": [47.5, 45.94, 41.5, 23.94, None],
            "plastic_limit_1_moisture_content": [26.5, 25.7, 23.3, 35.3, None],
            "plastic_limit_2_moisture_content": [27.0, 25.9, 23.8, 35.3, None],
            "plastic_limit": [26.7, 25.8, 23.6, 35.3, None],
            "is_nonplastic": [False, False, False, True, True],
            "plasticity_index": [20.8, 20.14, 17.9, None, None],
            "liquidity_index": [0.68, 0.40, 0.17, None, None],
        }
    ).convert_dtypes()


@pytest.mark.parametrize(
    ("method", "column", "rename", "kwargs"),
    [
        ("geotech.lab.index.get_moisture_content", "moisture_content", None, None),
        ("geotech.lab.index.get_liquid_limit", "liquid_limit", None, None),
        ("geotech.lab.index.get_plastic_limit", "plastic_limit", None, None),
        ("geotech.lab.index.is_nonplastic", "is_nonplastic", None, None),
        ("geotech.lab.index.get_plasticity_index", "plasticity_index", None, None),
        ("geotech.lab.index.get_liquidity_index", "liquidity_index", None, None),
    ],
)
def test_index_methods(df, method, column, rename, kwargs):
    """Test if the results of the `method` are equal with the contents of the `column`.

    Parameters
    ----------
    df: :external:class:`~pandas.DataFrame`
        DataFrame fixture.
    method: str
        Full method signature to call from `df`.
    column: str
        Column to extract from `df` for comparison.
    rename: str, optional
        Name to rename `column` with after extraction. If `None`, no renaming is done.
    kwargs: dict, optional
        Keyword argument dictionary to pass to `method`. If `None`, the method is called as is.
    """
    result = reduce(getattr, method.split("."), df)
    result = result() if kwargs is None else result(**kwargs)
    expected = df[column] if rename is None else df[column].rename(rename)
    tm.assert_series_equal(result, expected, check_exact=False, rtol=0.01, atol=0.01)
