"""Test ``spt`` subaccessor methods."""
from functools import reduce

import pandas as pd
import pandas._testing as tm
import pytest

from geotech_pandas.in_situ import SPTDataFrameAccessor


@pytest.fixture()
def df() -> pd.DataFrame:
    """Return common DataFrame for testing methods that return Series objects.

    This DataFrame is set up like a parametrized fixture where each point would expect a different
    outcome for each method in the spt subaccessor. The following are brief descriptions of each
    point:
    - normal: normal spt result
    - hw: hammer weight spt result
    - uds: uds sample, no spt processing should be done
    - ref_1: refusal with the partial penetration on the last interval
    - ref_2: refusal with the partial penetration on the second interval
    - ref_3: refusal with the partial penetration on the first interval
    - high: high N-value to test if `get_n_value(limit=True)` works as expected
    """
    return pd.DataFrame(
        {
            "point_id": ["normal", "hw", "uds", "ref_1", "ref_2", "ref_3", "high"],
            "bottom": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "sample_type": ["spt", "spt", "uds", "spt", "spt", "spt", "spt"],
            "sample_number": [1, 1, 1, 1, 1, 1, 1],
            "blows_1": [23, 0, None, 45, 43, 50, 49],
            "blows_2": [25, 0, None, 47, 50, None, 47],
            "blows_3": [24, 0, None, 50, None, None, 49],
            "pen_1": [150, 150, None, 150, 150, 50, 150],
            "pen_2": [150, 150, None, 150, 150, None, 150],
            "pen_3": [150, 150, None, 100, None, None, 150],
            "total_pen": [450, 450, None, 400, 300, 50, 450],
            "seating_drive": [23, 0, None, 45, 43, None, 49],
            "main_drive": [49, 0, None, 97, 50, None, 96],
            "n_value_1": [49, 0, None, 50, 50, 50, 96],
            "n_value_2": [49, 0, None, 50, 50, 50, 50],
        },
    ).convert_dtypes()


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.in_situ.spt, SPTDataFrameAccessor)


@pytest.mark.parametrize(
    ("method", "column", "rename", "kwargs"),
    [
        ("geotech.in_situ.spt.get_total_pen", "total_pen", None, None),
        ("geotech.in_situ.spt.get_seating_drive", "seating_drive", None, None),
        ("geotech.in_situ.spt.get_main_drive", "main_drive", None, None),
        ("geotech.in_situ.spt.get_n_value", "n_value_1", "n_value", None),
        ("geotech.in_situ.spt.get_n_value", "n_value_2", "n_value", {"limit": True}),
    ],
)
def test_spt_methods(df, method, column, rename, kwargs):
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
    tm.assert_series_equal(result, expected)


def test_get_n_value_warning(df):
    """Test if a warning is triggered when `refusal` is set to `pandas.NA` and `limit` is `True."""
    with pytest.warns(SyntaxWarning):
        df.geotech.in_situ.spt.get_n_value(refusal=pd.NA, limit=True)
