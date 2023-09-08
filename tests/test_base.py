"""Test base class methods."""

import pandas as pd
import pandas._testing as tm

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
