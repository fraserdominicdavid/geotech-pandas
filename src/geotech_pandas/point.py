"""A module containing a custom accessor for pandas that adds methods for depth related points."""

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

from geotech_pandas.base import GeotechPandasBase


class PointDataFrameAccessor(GeotechPandasBase):
    """
    An accessor class that contains methods for depth-related points.

    The dataframe should have ``point_id`` and ``bottom`` columns, where ``point_id`` would signify
    what group the ``bottom`` depths and other related data belong to. These groups can be accessed
    as a `DataFrameGroupBy` object through the `groups` property.
    """

    @property
    def groups(self) -> DataFrameGroupBy:
        """
        Return a pandas `DataFrameGroupBy` object based on the ``point_id`` column.

        This can be used a shortcut for grouping the dataframe by the ``point_id``.

        Returns
        -------
        DataFrameGroupBy
            GroupBy object that contains the grouped dataframes.
        """
        return self._obj.groupby("point_id")

    def get_group(self, point_id: str):
        """
        Return a `DataFrame` from the point groups with provided `point_id`.

        Parameters
        ----------
        point_id: str
            point_id of the group to get as a DataFrame.

        Returns
        -------
        DataFrame
            DataFrame that matches `point_id`.
        """
        return self.groups.get_group(point_id)

    def get_top(self, fill_value: float = 0.0) -> pd.Series:
        """Return shifted ``bottom`` depth values that can be used as ``top`` depth values.

        Parameters
        ----------
        fill_value: float, optional
            Float value to use for newly introduced missing values.

        Returns
        -------
        Series
            Series with shifted ``bottom`` values.
        """
        top = pd.Series(self.groups["bottom"].shift(1, fill_value=fill_value), name="top")
        return top

    def get_center(self) -> pd.Series:
        """Return ``center`` depth values from ``top`` and ``bottom`` depth values.

        Returns
        -------
        Series
            Series with ``center`` depth values.
        """
        self.validate_columns(self._obj, ["top", "bottom"])
        return pd.Series(self._obj[["top", "bottom"]].mean(axis=1), name="center")
