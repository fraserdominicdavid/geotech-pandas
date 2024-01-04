"""Test ``index`` subaccessor methods."""

import pandas as pd

from geotech_pandas.lab import IndexDataFrameAccessor


def test_accessor():
    """Test if accessor is registered correctly."""
    isinstance(pd.DataFrame.geotech.lab.index, IndexDataFrameAccessor)
