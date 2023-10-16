"""Subaccessor that contains methods for depth-related points."""

from typing import Union

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

from geotech_pandas.base import GeotechPandasBase


class PointDataFrameAccessor(GeotechPandasBase):
    """
    Subaccessor that contains methods for depth-related points.

    The :external:class:`~pandas.DataFrame` should have ``point_id`` and ``bottom`` columns, where
    ``point_id`` would signify what group the ``bottom`` depths and other related data belong to.
    These groups can be accessed as a :external:class:`~pandas.api.typing.DataFrameGroupBy` object
    through the :attr:`~DataFrame.geotech.point.groups` property.
    """

    @property
    def groups(self) -> DataFrameGroupBy:
        """
        Return a :external:class:`~pandas.api.typing.DataFrameGroupBy` object based on the
        ``point_id`` column.

        This can be used a shortcut for grouping the dataframe by the ``point_id``.

        Returns
        -------
        :external:class:`~pandas.api.typing.DataFrameGroupBy`
            GroupBy object that contains the grouped DataFrames.
        """  # noqa: D205
        return self._obj.groupby("point_id")

    def get_group(self, point_id: str):
        """
        Return a :external:class:`~pandas.DataFrame` from the point groups with provided `point_id`.

        Parameters
        ----------
        point_id: str
            point_id of the group to get as a DataFrame.

        Returns
        -------
        :external:class:`~pandas.DataFrame`
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
        :external:class:`~pandas.Series`
            Series with shifted ``bottom`` values.
        """
        top = pd.Series(self.groups["bottom"].shift(1, fill_value=fill_value), name="top")
        return top

    def get_center(self) -> pd.Series:
        """Return ``center`` depth values from ``top`` and ``bottom`` depth values.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with ``center`` depth values.
        """
        self._validate_columns(["top", "bottom"])
        return pd.Series(self._obj[["top", "bottom"]].mean(axis=1), name="center")

    def get_thickness(self) -> pd.Series:
        """Return ``thickness`` values of ``top`` and ``bottom`` depth values.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with ``thickness`` values.
        """
        self._validate_columns(["top", "bottom"])
        return pd.Series((self._obj["bottom"] - self._obj["top"]).abs(), name="thickness")

    def split_at_depth(
        self, depth: Union[pd.Series, float, int, str], reset_index: bool = True
    ) -> pd.DataFrame:
        """Split layers in the dataframe into two with the provided depth.

        If the provided depth is found in between the ``top`` and ``bottom`` columns of the
        dataframe, then those particular layers would be split.

        The ``top`` and ``bottom`` depths of the affected layers are also adjusted to have
        continuity after splitting. However, columns other than ``top`` and ``bottom`` are not
        modified. As such, it is recommended to split the layers before any depth-integrated
        calculations are done.

        This is particularly useful for cases where it is required or beneficial to split layers
        into two. For example, splitting a layer that is partly saturated and partly dry due to the
        groundwater level being found inside the layer.

        Parameters
        ----------
        depth: Series, float, int, or str
            The depth/s where the layer would be split.
        reset_index: bool, default True
            If `True`, resets the index after splitting.

        Returns
        -------
        :external:class:`~pandas.DataFrame`
            Dataframe with added and modified values for applicable layer splits. If no applicable
            splits are found, then the original dataframe is returned instead.
        """
        if isinstance(depth, str):
            validation_list = [depth, "top"]
            depth = self._obj[depth]
        else:
            validation_list = ["top"]
        self._validate_columns(validation_list)

        temp = self._obj.loc[(self._obj["top"] < depth) & (depth < self._obj["bottom"])].copy(
            deep=True
        )
        if temp.empty:
            return self._obj
        temp["bottom"] = depth
        temp = pd.concat([self._obj, temp])
        temp = temp.sort_values(["point_id", "bottom"])
        if reset_index:
            temp = temp.reset_index(drop=True)
        temp["top"] = temp.geotech.point.get_top()
        return temp
