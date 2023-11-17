"""Subaccessor that contains SPT-related methods."""

import pandas as pd

from geotech_pandas.base import GeotechPandasBase


class SPTDataFrameAccessor(GeotechPandasBase):
    """Subaccessor that contains methods related to the Standard Penetration Test (SPT)."""

    def __init__(self, accessor) -> None:
        super().__init__(accessor)
        self._validate_columns(
            [
                "sample_type",
                "sample_number",
                "blows_1",
                "blows_2",
                "blows_3",
                "pen_1",
                "pen_2",
                "pen_3",
            ]
        )

    def get_total_pen(self) -> pd.Series:
        """Return the total penetration of each interval."""
        return pd.Series(
            self._obj[["pen_1", "pen_2", "pen_3"]].sum(axis=1, min_count=1),
            name="total_pen",
        )
