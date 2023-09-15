"""A module containing a custom accessor for pandas that adds methods for depth related points."""

import pandas as pd
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

    def get_group(self, point_id: str):
        """
        Return a `DataFrame` from the point groups with provided `PointID`.

        Parameters
        ----------
        point_id: str
            PointID of the group to get as a DataFrame.

        Returns
        -------
        DataFrame
            DataFrame that matches `point_id`.
        """
        return self.groups.get_group(point_id)

    def get_top(self, fill_value: float = 0.0) -> pd.Series:
        """Return shifted ``Bottom`` depth values that can be used as ``Top`` depth values.

        Parameters
        ----------
        fill_value: float, optional
            Float value to use for newly introduced missing values.

        Returns
        -------
        Series
            Series with shifted ``Bottom`` values.
        """
        top = pd.Series(self.groups["Bottom"].shift(1, fill_value=fill_value), name="Top")
        return top
