"""Subaccessor that contains SPT-related methods."""

import warnings

import pandas as pd

from geotech_pandas.base import GeotechPandasBase

PEN_INC_MIN = 150
PEN_TOTAL_MIN = 450


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

    def get_seating_pen(self) -> pd.Series:
        """Return the seating penetration from the first interval of each sample.

        Only full penetrations of 150 mm are returned, where partial penetrations are masked with
        `NA`.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with seating penetration values.
        """
        seating_pen = self._obj["pen_1"].convert_dtypes()
        seating_pen[seating_pen.ne(PEN_INC_MIN)] = pd.NA
        return pd.Series(seating_pen, name="seating_pen")

    def get_main_pen(self) -> pd.Series:
        """Return the total penetration in the second and third 150 mm interval for each sample.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with main penetration values.
        """
        return pd.Series(
            self._obj[["pen_2", "pen_3"]].sum(axis=1, min_count=1),
            name="main_pen",
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
        seating_drive[self.get_seating_pen().isna()] = pd.NA
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

    def get_total_drive(self) -> pd.Series:
        """Return the sum of the number of blows in all three 150 mm intervals of each sample.

        The sum is still returned regardless of the completeness of each interval.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with total drive values.
        """
        return pd.Series(
            self._obj[["blows_1", "blows_2", "blows_3"]].sum(axis=1, min_count=1),
            name="total_drive",
        )

    def get_n_value(self, refusal=50, limit=False) -> pd.Series:
        """Return the N-value for each sample.

        When the total penetration is less than 450 mm, the N-value is assumed as `refusal`. If
        `limit` is set to `True`, then any N-value exceeding `refusal` will be limited to `refusal`.

        .. warning::

            If `limit` is `True` while `refusal` is set to :external:attr:`~pandas.NA`,
            nothing will get limited.

        Parameters
        ----------
        refusal: int
            Equivalent N-value for samples with total penetration less than 450 mm.
        limit: bool, default False
            If `True`, limits the resulting N-value to `refusal`.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with N-values.
        """
        n_value = self.get_main_drive()
        n_value.loc[self.get_total_pen() < PEN_TOTAL_MIN] = refusal
        if limit:
            if refusal is pd.NA:
                warnings.warn(
                    f"Limiting the N-value with {refusal} will not do anything. "
                    f"If you want to limit the N-value, make sure that `refusal` is set correctly.",
                    stacklevel=2,
                    category=SyntaxWarning,
                )
            n_value.loc[n_value > refusal] = refusal
        return pd.Series(n_value, name="n_value")
