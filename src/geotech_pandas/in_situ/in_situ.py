"""General subaccessor for in-situ test subaccessors."""

from geotech_pandas.base import GeotechPandasBase
from geotech_pandas.in_situ.spt import SPTDataFrameAccessor
from geotech_pandas.utils import SubAccessor


class InSituDataFrameAccessor(GeotechPandasBase):
    """General subaccessor that contains various subaccessors that handle in-situ test data."""

    spt = SubAccessor(SPTDataFrameAccessor)
