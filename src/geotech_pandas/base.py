"""A module containing a common class used throughout the geotech-pandas package."""

import pandas as pd


class GeotechPandasBase:
    """A base class with common validation methods for dataframes."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._obj = df
