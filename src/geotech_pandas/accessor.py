"""General dataframe accessor class for the Geotech Pandas package."""

import pandas as pd

from geotech_pandas.point import PointDataFrameAccessor


@pd.api.extensions.register_dataframe_accessor("geotech")
class GeotechDataFrameAccessor:
    """DataFrame accessor that provides namespaces to the various accessors in Geotech Pandas."""

    def __init__(self, df: pd.DataFrame):
        self.point: PointDataFrameAccessor = PointDataFrameAccessor(df)
        """Accessor for depth-related points."""
