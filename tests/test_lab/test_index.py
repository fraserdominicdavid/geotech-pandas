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
            "point_id": ["bh-1", "bh-2", "bh-3", "None"],
            "bottom": [1, 1, 1, 1],
            "moisture_content_mass_moist": [236.44, 154.40, 164.68, None],
            "moisture_content_mass_dry": [174.40, 120.05, 134.31, None],
            "moisture_content_mass_container": [22.20, 18.66, 20.27, None],
            "moisture_content": [40.76, 33.88, 26.63, None],
        }
    ).convert_dtypes()


@pytest.mark.parametrize(
    ("method", "column", "rename", "kwargs"),
    [
        ("geotech.lab.index.get_moisture_content", "moisture_content", None, None),
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
