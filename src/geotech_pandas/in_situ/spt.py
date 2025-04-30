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

        .. admonition:: **Requires:**
            :class: important

            | :term:`pen_1`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`seating_pen`
        """
        seating_pen = self._obj["pen_1"].convert_dtypes()
        seating_pen[seating_pen.ne(PEN_INC_MIN)] = pd.NA
        return pd.Series(seating_pen, name="seating_pen")

    def get_main_pen(self) -> pd.Series:
        """Return the total penetration in the second and third 150 mm increment for each sample.

        .. admonition:: **Requires:**
            :class: important

            | :term:`pen_2`
            | :term:`pen_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`main_pen`
        """
        return pd.Series(
            self._obj[["pen_2", "pen_3"]].sum(axis=1, min_count=1),
            name="main_pen",
        )

    def get_total_pen(self) -> pd.Series:
        """Return the total penetration of each increment.

        .. admonition:: **Requires:**
            :class: important

            | :term:`pen_1`
            | :term:`pen_2`
            | :term:`pen_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`total_pen`
        """
        return pd.Series(
            self._obj[["pen_1", "pen_2", "pen_3"]].sum(axis=1, min_count=1),
            name="total_pen",
        )

    def get_seating_drive(self) -> pd.Series:
        """Return the number of blows in the first 150 mm increment for each sample.

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_1`
            | :term:`pen_1`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`seating_drive`

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

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_2`
            | :term:`blows_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`main_drive`
        """
        return pd.Series(
            self._obj[["blows_2", "blows_3"]].sum(axis=1, min_count=1),
            name="main_drive",
        )

    def get_total_drive(self) -> pd.Series:
        """Return the sum of the number of blows in all three 150 mm increments of each sample.

        The sum is still returned regardless of the completeness of each increment.

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_1`
            | :term:`blows_2`
            | :term:`blows_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`total_drive`
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

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_1`
            | :term:`blows_2`
            | :term:`blows_3`
            | :term:`pen_1`
            | :term:`pen_2`
            | :term:`pen_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`is_refusal`
        """
        return pd.Series(
            self._any_blows_max_inc() | self._any_blows_max_total() | self._any_pen_partial(),
            name="is_refusal",
        )

    def is_hammer_weight(self) -> pd.Series:
        """Return whether or not each sample is hammer weight.

        A sample is considered hammer weight when all of the following are true:

        - a total of 450 mm or more was penetrated by the sampler through sinking; and
        - each 150 mm increment has 0 blows recorded.

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_1`
            | :term:`blows_2`
            | :term:`blows_3`
            | :term:`pen_1`
            | :term:`pen_2`
            | :term:`pen_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`is_hammer_weight`
        """
        return pd.Series(
            (self._obj[["blows_1", "blows_2", "blows_3"]].eq(0)).all(axis=1)
            & (self.get_total_pen() >= PEN_TOTAL_MIN),
            name="is_hammer_weight",
        )

    def get_n_value(self, refusal=50, limit=False) -> pd.Series:
        """Return the N-value for each sample.

        When a sample is a refusal, then the N-value is assumed as the value set in `refusal`. If
        `limit` is set to `True`, then any N-value exceeding `refusal` will be limited to `refusal`.

        .. warning::

            If `limit` is `True` while `refusal` is set to :external:attr:`~pandas.NA`,
            nothing will get limited.

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_1`
            | :term:`blows_2`
            | :term:`blows_3`
            | :term:`pen_1`
            | :term:`pen_2`
            | :term:`pen_3`

        Parameters
        ----------
        refusal: int, default 50
            Equivalent N-value for samples with total penetration less than 450 mm.
        limit: bool, default False
            If `True`, limits the resulting N-value to `refusal`.

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`n_value`
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

    def _format_blows(self, interval) -> pd.Series:
        _blows = self._obj[f"blows_{interval}"]
        _pen = self._obj[f"pen_{interval}"]

        _m = _pen < PEN_INC_MIN

        _blows = _blows.astype("string")
        _pen = _pen.astype("string")

        _blows[_m] = _blows[_m] + "/" + _pen[_m] + "mm"
        _blows.name = f"_format_blows_{interval}"
        return _blows

    def _cat_blows(self) -> pd.Series:
        _blows_1 = self._format_blows(1)
        _blows_2 = self._format_blows(2)
        _blows_3 = self._format_blows(3)

        _blows = _blows_1.str.cat([_blows_2, _blows_3], sep=",", na_rep="-")
        _blows = _blows.replace("-,-,-", pd.NA)
        _blows.name = "_cat_blows"
        return _blows

    def _format_n_value(self) -> pd.Series:
        _n_value = "N=" + self.get_main_drive().astype("string")

        _m = self.get_main_pen() < 2 * PEN_INC_MIN
        _n_value[_m] = _n_value[_m] + "/" + self.get_main_pen()[_m].astype("string") + "mm"

        _m = self.get_total_pen() <= PEN_INC_MIN
        _n_value[_m] = "N="

        _m = self.is_refusal()
        _n_value[_m] = _n_value[_m] + "(R)"

        _m = self.is_hammer_weight()
        _n_value[_m] = _n_value[_m] + "(HW)"

        _n_value.name = "_format_n_value"
        return _n_value

    def get_report(self) -> pd.Series:
        """Return descriptive strings that show the blows per interval and N-value.

        The format of the strings follows this convention,
        ``{blows_1},{blows_2},{blows_3} N={n_value}{remark}``, where the remark can be defined as
        follows:

         - ``(HW)`` for hammer weight samples
         - ``(R)`` for refusal samples

        .. admonition:: **Requires:**
            :class: important

            | :term:`blows_1`
            | :term:`blows_2`
            | :term:`blows_3`
            | :term:`pen_1`
            | :term:`pen_2`
            | :term:`pen_3`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`spt_report`
        """
        return pd.Series(
            self._cat_blows().str.cat(self._format_n_value(), sep=" "),
            name="spt_report",
        ).convert_dtypes()

    def get_typical_hammer_efficiency_factor(self) -> pd.Series:
        """Return the typical hammer efficiency factor based on country, type, and release.

        The efficiency factor is used to convert the N-value to a corrected N-value. The hammer
        efficiency factor is based on the following conditions (country, type, and release):

        .. list-table:: Typical Hammer Efficiency Factors
            :header-rows: 1

            * - Country
              - Hammer Type
              - Hammer Release
              - Efficiency Factor
            * - Japan (jp)
              - donut hammer
              - free fall
              - 0.78
            * - Japan (jp)
              - donut hammer
              - rope and pulley
              - 0.67
            * - United States (us)
              - safety hammer
              - rope and pulley
              - 0.60
            * - United States (us)
              - donut hammer
              - rope and pulley
              - 0.45
            * - Argentina (ar)
              - donut hammer
              - rope and pulley
              - 0.45
            * - China (cn)
              - donut hammer
              - free fall
              - 0.60
            * - China (cn)
              - donut hammer
              - rope and pulley
              - 0.50

        The country mentioned here refers to the referenced country of the SPT practice, not the
        location of the test. This is because SPT practice is not standardized worldwide and the
        methodology used in each country causes the variation in the hammer efficiency factor.

        If any value in the required columns is `NA`, then the efficiency factor will also be `NA`.

        .. admonition:: **Requires:**
            :class: important

            | :term:`spt_hammer_country_ref`
            | :term:`spt_hammer_type`
            | :term:`spt_hammer_release`

        Returns
        -------
        :external:class:`~pandas.Series`
            :term:`spt_hammer_efficiency_factor`
        """
        self._validate_column_values("spt_hammer_country_ref", ["jp", "us", "ar", "cn"])
        self._validate_column_values("spt_hammer_type", ["donut hammer", "safety hammer"])
        self._validate_column_values("spt_hammer_release", ["free fall", "rope and pulley"])

        caselist = [
            # None
            (
                (self._obj["spt_hammer_country_ref"].isna())
                | (self._obj["spt_hammer_type"].isna())
                | (self._obj["spt_hammer_release"].isna()),
                pd.NA,
            ),
            # Japan
            (
                (self._obj["spt_hammer_country_ref"] == "jp")
                & (self._obj["spt_hammer_type"] == "donut hammer")
                & (self._obj["spt_hammer_release"] == "free fall"),
                0.78,
            ),
            (
                (self._obj["spt_hammer_country_ref"] == "jp")
                & (self._obj["spt_hammer_type"] == "donut hammer")
                & (self._obj["spt_hammer_release"] == "rope and pulley"),
                0.67,
            ),
            # United States
            (
                (self._obj["spt_hammer_country_ref"] == "us")
                & (self._obj["spt_hammer_type"] == "safety hammer")
                & (self._obj["spt_hammer_release"] == "rope and pulley"),
                0.60,
            ),
            (
                (self._obj["spt_hammer_country_ref"] == "us")
                & (self._obj["spt_hammer_type"] == "donut hammer")
                & (self._obj["spt_hammer_release"] == "rope and pulley"),
                0.45,
            ),
            # Argentina
            (
                (self._obj["spt_hammer_country_ref"] == "ar")
                & (self._obj["spt_hammer_type"] == "donut hammer")
                & (self._obj["spt_hammer_release"] == "rope and pulley"),
                0.45,
            ),
            # China
            (
                (self._obj["spt_hammer_country_ref"] == "cn")
                & (self._obj["spt_hammer_type"] == "donut hammer")
                & (self._obj["spt_hammer_release"] == "free fall"),
                0.60,
            ),
            (
                (self._obj["spt_hammer_country_ref"] == "cn")
                & (self._obj["spt_hammer_type"] == "donut hammer")
                & (self._obj["spt_hammer_release"] == "rope and pulley"),
                0.50,
            ),
        ]

        spt_hammer_efficiency_factor = pd.Series(
            pd.NA,
            index=self._obj.index,
            name="spt_hammer_efficiency_factor",
        )

        # Ignore mypy error which detects incompatible type "list[tuple[Series[bool], object]]" for
        # the caselist arg of the case_when method. Possibly raise an issue in pandas.
        spt_hammer_efficiency_factor = spt_hammer_efficiency_factor.case_when(caselist)  # type: ignore[arg-type]
        spt_hammer_efficiency_factor = spt_hammer_efficiency_factor.astype("Float64")

        return spt_hammer_efficiency_factor
