"""A module containing a custom accessor for pandas that adds methods for depth related points."""

from pandas.core.groupby.generic import DataFrameGroupBy

from geotech_pandas.base import GeotechPandasBase


class PointDataFrameAccessor(GeotechPandasBase):
    """
    An accessor class that contains methods for depth-related points.

    The dataframe should have ``PointID`` and ``Bottom`` columns, where ``PointID`` would signify
    what group the ``Bottom`` depths and other related data belong to. These groups can be accessed
    as a `DataFrameGroupBy` object through the `groups` property.
    """

    @property
    def groups(self) -> DataFrameGroupBy:
        """
        Return a pandas `DataFrameGroupBy` object based on the ``PointID`` column.

        This can be used a shortcut for grouping the dataframe by the ``PointID``.

        Returns
        -------
        DataFrameGroupBy
            GroupBy object that contains the grouped dataframes.
        """
        return self._obj.groupby("PointID")
