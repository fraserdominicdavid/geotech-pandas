"""Subaccessor that contains SPT-related methods."""

import pandas as pd

from geotech_pandas.base import GeotechPandasBase


class SPTDataFrameAccessor(GeotechPandasBase):
    """Subaccessor that contains methods related to the Standard Penetration Test (SPT)."""

    def __init__(self, accessor) -> None:
        super().__init__(accessor)
        self._validate_columns(
            [
                "sample_type",
                "sample_number",
                "blows_1",
                "blows_2",
                "blows_3",
                "pen_1",
                "pen_2",
                "pen_3",
            ]
        )

    def get_total_pen(self) -> pd.Series:
        """Return the total penetration of each interval.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with total penetration values.
        """
        return pd.Series(
            self._obj[["pen_1", "pen_2", "pen_3"]].sum(axis=1, min_count=1),
            name="total_pen",
        )

    def get_seating_drive(self) -> pd.Series:
        """Return the number of blows in the first 150 mm interval for each sample.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with seating drive values.

        Notes
        -----
        The seating drive is defined as the first 150 mm interval driven by the sampler, therefore,
        only the number of blows of samples with ``pen_1`` equal to 150 mm are taken.
        """
        seating_drive = self._obj["blows_1"].convert_dtypes()
        seating_drive.loc[self._obj["pen_1"].ne(150)] = pd.NA
        return pd.Series(seating_drive, name="seating_drive")

    def get_main_drive(self) -> pd.Series:
        """Return the total blows in the second and third 150 mm interval for each sample.

        The sum is still returned regardless of the completeness of each interval. Due to this, the
        results may not correspond to the reported N-value.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with main drive values.
        """
        return pd.Series(
            self._obj[["blows_2", "blows_3"]].sum(axis=1, min_count=1),
            name="main_drive",
        )
