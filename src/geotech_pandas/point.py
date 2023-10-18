"""Subaccessor that contains point-related methods."""

from pandas.core.groupby.generic import DataFrameGroupBy

from geotech_pandas.base import GeotechPandasBase


class PointDataFrameAccessor(GeotechPandasBase):
    """
    Subaccessor that contains point-related methods.

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

        This can be used as a shortcut for grouping the :external:class:`~pandas.DataFrame` by the
        ``point_id``.

        Returns
        -------
        :external:class:`~pandas.api.typing.DataFrameGroupBy`
            GroupBy object that contains the grouped DataFrame objects.
        """  # noqa: D205
        return self._obj.groupby("point_id")

    def get_group(self, point_id: str):
        """
        Return a :external:class:`~pandas.DataFrame` from the point groups with matching
        ``point_id``.

        Parameters
        ----------
        point_id: str
            point_id of the group to get as a DataFrame.

        Returns
        -------
        :external:class:`~pandas.DataFrame`
            DataFrame that matches ``point_id``.
        """  # noqa: D205
        return self.groups.get_group(point_id)
