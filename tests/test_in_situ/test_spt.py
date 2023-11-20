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
    """
    return pd.DataFrame(
        {
            "point_id": ["normal", "hw", "uds", "ref_1", "ref_2", "ref_3"],
            "bottom": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            "sample_type": ["spt", "spt", "uds", "spt", "spt", "spt"],
            "sample_number": [1, 1, 1, 1, 1, 1],
            "blows_1": [23, 0, None, 45, 43, 50],
            "blows_2": [25, 0, None, 47, 50, None],
            "blows_3": [24, 0, None, 50, None, None],
            "pen_1": [150, 150, None, 150, 150, 50],
            "pen_2": [150, 150, None, 150, 150, None],
            "pen_3": [150, 150, None, 100, None, None],
            "total_pen": [450, 450, None, 400, 300, 50],
            "seating_drive": [23, 0, None, 45, 43, None],
            "main_drive": [49, 0, None, 97, 50, None],
        },
    ).convert_dtypes()


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.in_situ.spt, SPTDataFrameAccessor)


@pytest.mark.parametrize(
    ("method", "column"),
    [
        ("geotech.in_situ.spt.get_total_pen", "total_pen"),
        ("geotech.in_situ.spt.get_seating_drive", "seating_drive"),
        ("geotech.in_situ.spt.get_main_drive", "main_drive"),
    ],
)
def test_spt_methods(df, method, column):
    """Test if the results of the method are equal with the contents of the column."""
    tm.assert_series_equal(reduce(getattr, method.split("."), df)(), df[column])
