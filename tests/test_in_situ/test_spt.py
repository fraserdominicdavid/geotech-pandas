"""Test ``spt`` subaccessor methods."""

from functools import reduce

import pandas as pd
import pandas._testing as tm
import pytest

from geotech_pandas.in_situ import SPTDataFrameAccessor


@pytest.fixture
def df() -> pd.DataFrame:
    """Return common DataFrame for testing methods that return Series objects.

    This DataFrame is set up like a parametrized fixture where each point would expect a different
    outcome for each method in the spt subaccessor. The following are brief descriptions of each
    point:
    - normal: normal spt result
    - hw: hammer weight spt result
    - uds: uds sample, no spt processing should be done
    - ref_1: refusal with the partial penetration on the last increment
    - ref_2: refusal with the partial penetration on the second increment
    - ref_3: refusal with the partial penetration on the first increment
    - high: high N-value to test if `get_n_value(limit=True)` works as expected
    - #96: test issue #96
    """
    return pd.DataFrame(
        {
            "point_id": ["normal", "hw", "uds", "ref_1", "ref_2", "ref_3", "high", "#96"],
            "bottom": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "sample_type": ["spt", "spt", "uds", "spt", "spt", "spt", "spt", "spt"],
            "sample_number": [1, 1, 1, 1, 1, 1, 1, 1],
            "blows_1": [23, 0, None, 45, 43, 50, 23, 50],
            "blows_2": [25, 0, None, 47, 50, None, 29, None],
            "blows_3": [24, 0, None, 50, None, None, 35, None],
            "pen_1": [150, 150, None, 150, 150, 50, 150, 150],
            "pen_2": [150, 150, None, 150, 150, None, 150, None],
            "pen_3": [150, 150, None, 100, None, None, 150, None],
            "seating_pen": [150, 150, None, 150, 150, None, 150, 150],
            "main_pen": [300, 300, None, 250, 150, None, 300, None],
            "total_pen": [450, 450, None, 400, 300, 50, 450, 150],
            "seating_drive": [23, 0, None, 45, 43, None, 23, 50],
            "main_drive": [49, 0, None, 97, 50, None, 64, None],
            "total_drive": [72, 0, None, 142, 93, 50, 87, 50],
            "_any_blows_max_inc": [False, False, None, True, True, True, False, True],
            "_any_blows_max_total": [False, False, None, True, False, False, False, False],
            "_any_pen_partial": [False, False, None, True, True, True, False, True],
            "is_refusal": [False, False, None, True, True, True, False, True],
            "is_hammer_weight": [False, True, None, False, False, False, False, False],
            "n_value_1": [49, 0, None, 50, 50, 50, 64, 50],
            "n_value_2": [49, 0, None, 50, 50, 50, 50, 50],
            "_format_blows_1": ["23", "0", None, "45", "43", "50/50mm", "23", "50"],
            "_format_blows_2": ["25", "0", None, "47", "50", None, "29", None],
            "_format_blows_3": ["24", "0", None, "50/100mm", None, None, "35", None],
            "_cat_blows": [
                "23,25,24",
                "0,0,0",
                None,
                "45,47,50/100mm",
                "43,50,-",
                "50/50mm,-,-",
                "23,29,35",
                "50,-,-",
            ],
            "_format_n_value": [
                "N=49",
                "N=0(HW)",
                None,
                "N=97/250mm(R)",
                "N=50/150mm(R)",
                "N=(R)",
                "N=64",
                "N=(R)",
            ],
            "spt_report": [
                "23,25,24 N=49",
                "0,0,0 N=0(HW)",
                None,
                "45,47,50/100mm N=97/250mm(R)",
                "43,50,- N=50/150mm(R)",
                "50/50mm,-,- N=(R)",
                "23,29,35 N=64",
                "50,-,- N=(R)",
            ],
        },
    ).convert_dtypes()


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.in_situ.spt, SPTDataFrameAccessor)


@pytest.mark.parametrize(
    ("method", "column", "rename", "kwargs"),
    [
        ("geotech.in_situ.spt.get_seating_pen", "seating_pen", None, None),
        ("geotech.in_situ.spt.get_main_pen", "main_pen", None, None),
        ("geotech.in_situ.spt.get_total_pen", "total_pen", None, None),
        ("geotech.in_situ.spt.get_seating_drive", "seating_drive", None, None),
        ("geotech.in_situ.spt.get_main_drive", "main_drive", None, None),
        ("geotech.in_situ.spt.get_total_drive", "total_drive", None, None),
        ("geotech.in_situ.spt._any_blows_max_inc", "_any_blows_max_inc", None, None),
        ("geotech.in_situ.spt._any_blows_max_total", "_any_blows_max_total", None, None),
        ("geotech.in_situ.spt._any_pen_partial", "_any_pen_partial", None, None),
        ("geotech.in_situ.spt.is_refusal", "is_refusal", None, None),
        ("geotech.in_situ.spt.is_hammer_weight", "is_hammer_weight", None, None),
        ("geotech.in_situ.spt.get_n_value", "n_value_1", "n_value", None),
        ("geotech.in_situ.spt.get_n_value", "n_value_2", "n_value", {"limit": True}),
        ("geotech.in_situ.spt._format_blows", "_format_blows_1", None, {"interval": 1}),
        ("geotech.in_situ.spt._format_blows", "_format_blows_2", None, {"interval": 2}),
        ("geotech.in_situ.spt._format_blows", "_format_blows_3", None, {"interval": 3}),
        ("geotech.in_situ.spt._cat_blows", "_cat_blows", None, None),
        ("geotech.in_situ.spt._format_n_value", "_format_n_value", None, None),
        ("geotech.in_situ.spt.get_report", "spt_report", None, None),
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


def test_any_with_na_error(df):
    """Test if a `ValueError` is raised when passing on arguments with differnt shapes."""
    values = df[["blows_1", "blows_2", "blows_3"]]
    max_value = 100
    mask = df[["blows_2", "blows_3"]] >= max_value
    with pytest.raises(ValueError, match="`values` and `mask` must have the same shape."):
        df.geotech.in_situ.spt._any_with_na_rows(values, mask)
