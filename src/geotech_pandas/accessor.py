"""General :external:class:`~pandas.DataFrame` accessor for the geotech-pandas package."""

import pandas as pd

from geotech_pandas.base import GeotechPandasBase
from geotech_pandas.in_situ import InSituDataFrameAccessor
from geotech_pandas.layer import LayerDataFrameAccessor
from geotech_pandas.point import PointDataFrameAccessor
from geotech_pandas.utils import SubAccessor


@pd.api.extensions.register_dataframe_accessor("geotech")
class GeotechDataFrameAccessor(GeotechPandasBase):
    """:external:class:`~pandas.DataFrame` accessor that provides namespaces to the various
    subaccessors in geotech-pandas.
    """  # noqa: D205

    point = SubAccessor(PointDataFrameAccessor)
    layer = SubAccessor(LayerDataFrameAccessor)
    in_situ = SubAccessor(InSituDataFrameAccessor)

    def __init__(self, df: pd.DataFrame):
        self._obj = df

        self._validate_columns()
        self._validate_monotony()
        self._validate_duplicates()
