"""General subaccessor for laboratory test subaccessors."""

from geotech_pandas.base import GeotechPandasBase
from geotech_pandas.lab.index import IndexDataFrameAccessor
from geotech_pandas.utils import SubAccessor


class LabDataFrameAccessor(GeotechPandasBase):
    """General subaccessor that contains various subaccessors that handle laboratory test data."""

    index = SubAccessor(IndexDataFrameAccessor)
