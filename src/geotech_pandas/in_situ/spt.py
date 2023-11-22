"""Subaccessor that contains SPT-related methods."""

import warnings

import pandas as pd

from geotech_pandas.base import GeotechPandasBase

PEN_INC_MIN = 150
PEN_TOTAL_MIN = 450
BLOWS_INC_MAX = 50
BLOWS_TOTAL_MAX = 100


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
        """Return the seating penetration from the first increment of each sample.

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
        """Return the total penetration in the second and third 150 mm increment for each sample.

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
        """Return the total penetration of each increment.

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
        """Return the number of blows in the first 150 mm increment for each sample.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with seating drive values.

        Notes
        -----
        The seating drive is defined as the first 150 mm increment driven by the sampler, therefore,
        only the number of blows of samples with ``pen_1`` equal to 150 mm are taken.
        """
        seating_drive = self._obj["blows_1"].convert_dtypes()
        seating_drive[self.get_seating_pen().isna()] = pd.NA
        return pd.Series(seating_drive, name="seating_drive")

    def get_main_drive(self) -> pd.Series:
        """Return the total blows in the second and third 150 mm increment for each sample.

        The sum is still returned regardless of the completeness of each increment. Due to this, the
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
        """Return the sum of the number of blows in all three 150 mm increments of each sample.

        The sum is still returned regardless of the completeness of each increment.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with total drive values.
        """
        return pd.Series(
            self._obj[["blows_1", "blows_2", "blows_3"]].sum(axis=1, min_count=1),
            name="total_drive",
        )

    def _any_with_na_rows(self, values: pd.DataFrame, mask: pd.DataFrame) -> pd.Series:
        """Return whether any element is `True` in `mask` while preserving `NA` from `values`.

        `NA` will only be preserved if all elements in a row are `NA`.

        Parameters
        ----------
        values: DataFrame
            Values to check for `NA` rows.
        mask: DataFrame
            `values` mask where the `NA` rows are applied.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series whether any element is `True` in `mask`, with preserved `NA` rows.
        """
        if values.shape != mask.shape:
            raise ValueError("`values` and `mask` must have the same shape.")

        _na = values.isna().all(axis=1)
        _values = mask.any(axis=1)
        _values[_na] = pd.NA
        return _values

    def _any_blows_max_inc(self) -> pd.Series:
        _values = self._obj[["blows_1", "blows_2", "blows_3"]]
        return pd.Series(
            self._any_with_na_rows(_values, (_values >= BLOWS_INC_MAX)),
            name="_any_blows_max_inc",
        )

    def _any_blows_max_total(self) -> pd.Series:
        return pd.Series(
            self.get_total_drive() >= BLOWS_TOTAL_MAX,
            name="_any_blows_max_total",
        )

    def _any_pen_partial(self) -> pd.Series:
        _values = self._obj[["pen_1", "pen_2", "pen_3"]]
        return pd.Series(
            self._any_with_na_rows(_values, (_values < PEN_INC_MIN) | (_values.isna())),
            name="_any_pen_partial",
        )

    def is_refusal(self) -> pd.Series:
        """Return whether or not each sample is a refusal.

        A sample is considered a refusal when any of the following is true:

         - a total of 50 blows or more have been applied during any of the three 150 mm increments;
         - a total of 100 blows or more have been applied; and
         - partial penetration, which signifies that the sampler can no longer penetrate through the
           strata, is present in any of the increments.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series of booleans indicating whether or not each sample is refused.
        """
        return pd.Series(
            self._any_blows_max_inc() | self._any_blows_max_total() | self._any_pen_partial(),
            name="is_refusal",
        )

    def get_n_value(self, refusal=50, limit=False) -> pd.Series:
        """Return the N-value for each sample.

        When a sample is a refusal, then the N-value is assumed as the value set in `refusal`. If
        `limit` is set to `True`, then any N-value exceeding `refusal` will be limited to `refusal`.

        .. warning::

            If `limit` is `True` while `refusal` is set to :external:attr:`~pandas.NA`,
            nothing will get limited.

        Parameters
        ----------
        refusal: int, default 50
            Equivalent N-value for samples with total penetration less than 450 mm.
        limit: bool, default False
            If `True`, limits the resulting N-value to `refusal`.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with N-values.
        """
        n_value = self.get_main_drive()
        n_value.loc[self.is_refusal()] = refusal
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
