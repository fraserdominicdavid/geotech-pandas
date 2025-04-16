"""Subaccessor that contains methods related to index property tests."""

import numpy as np
import pandas as pd

from geotech_pandas.base import GeotechPandasBase
from geotech_pandas.helpers import _get_linear_forecast


class IndexDataFrameAccessor(GeotechPandasBase):
    """Subaccessor that contains methods related to index property tests.

    The index properties of soil are the properties which help to assess the engineering behavior of
    soil and determine the classification of soil accurately.

    Notes
    -----
    The index properties of soil are important for understanding the physical and chemical
    characteristics of soil. They are used to classify soil and predict its behavior under different
    conditions. These properties are determined through laboratory tests, some key properties
    include:

    - moisture content [1]_
    - consistency or Atterberg limits [2]_
    - particle size distribution
    - specific gravity
    - soil classification

    References
    ----------
    .. [1] ASTM International. (2019). *Standard test methods for laboratory determination of
           water (moisture) content of soil and rock by mass* (ASTM D2216-19).
           https://doi.org/10.1520/D2216-19
    .. [2] ASTM International. (2018). *Standard test methods for liquid limit, plastic limit,
           and plasticity index of soils* (ASTM D4318-17e1).
           https://doi.org/10.1520/D4318-17E01
    """

    def get_moisture_content(self, prefix="moisture_content") -> pd.Series:
        r"""Calculate and return the moisture content according to ASTM D2216.

        This method allows the use of `prefix` where it is possible to specify the prefix and name
        used for calculating the moisture content. This is useful for other moisture content
        applications like the Atterberg limits.

        .. admonition:: **Requires:**
            :class: important

            | :term:`{prefix}_mass_moist`
            | :term:`{prefix}_mass_dry`
            | :term:`{prefix}_mass_container`

        Parameters
        ----------
        prefix: string, default "moisture_content"
            Prefix to use for looking up the relevant columns. This is also used as the prefix of
            the name of the resulting series if using a non-default value.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with moisture content values.

        Notes
        -----
        In general, the moisture content, :math:`w`, is calculated by:

        .. math:: w = \frac{M_{cms} - M_{cds}}{M_{cds} - M_c} \times 100

        where:

        - :math:`w =` moisture content, %,
        - :math:`M_{cms} =` mass of container and moist specimen, g,
        - :math:`M_{cds} =` mass of container and oven dry specimen, g,
        - :math:`M_{c} =` mass of container, g,

        .. note::

           ASTM D2216 offers two methods in determining the moisture content, however, the major
           difference is only in the rounding of the result (by 1% or 0.1%). This is not covered
           by this method so the user can provide their own rounding based on their specific use.

        References
        ----------
        .. [1] ASTM International. (2019). *Standard test methods for laboratory determination of
           water (moisture) content of soil and rock by mass* (ASTM D2216-19).
           https://doi.org/10.1520/D2216-19

        Examples
        --------
        Getting the moisture content:

        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1"],
        ...         "bottom": [1.0],
        ...         "moisture_content_mass_moist": [236.44],
        ...         "moisture_content_mass_dry": [174.40],
        ...         "moisture_content_mass_container": [22.20],
        ...     }
        ... )
        >>> df.geotech.lab.index.get_moisture_content(prefix="moisture_content")
        0    40.762155
        Name: moisture_content, dtype: float64

        Getting the moisture content with `prefix="liquid_limit_1"`:

        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1"],
        ...         "bottom": [1.0],
        ...         "liquid_limit_1_mass_moist": [23.51],
        ...         "liquid_limit_1_mass_dry": [17.85],
        ...         "liquid_limit_1_mass_container": [3.30],
        ...     }
        ... )
        >>> df.geotech.lab.index.get_moisture_content(prefix="liquid_limit_1")
        0    38.900344
        Name: liquid_limit_1_moisture_content, dtype: float64
        """
        columns = [f"{prefix}_mass_moist", f"{prefix}_mass_dry", f"{prefix}_mass_container"]
        self._validate_columns(columns)

        moist = self._obj[columns[0]]
        dry = self._obj[columns[1]]
        container = self._obj[columns[2]]
        prefix = f"{prefix}_moisture_content" if prefix != "moisture_content" else prefix
        moisture_content = pd.Series((moist - dry) / (dry - container) * 100, name=prefix)

        return moisture_content

    def _prepare_liquid_limit_data(self, trials: int) -> list[str]:
        """Prepare and validate the required columns for liquid limit calculations.

        This method generates a list of column names based on the number of trials and validates
        their existence in the DataFrame.

        .. admonition:: **Requires:**
            :class: important

            | :term:`liquid_limit_{n}_drops`
            | :term:`liquid_limit_{n}_moisture_content`

        Parameters
        ----------
        trials: int
            The number of trials to include in the liquid limit calculation.

        Returns
        -------
        list[str]
            A list of column names required for liquid limit calculations.
        """
        columns = ["point_id", "bottom"]
        for n in range(trials):
            columns.extend(
                [
                    f"liquid_limit_{n + 1}_drops",
                    f"liquid_limit_{n + 1}_moisture_content",
                ]
            )
        self._validate_columns(columns)
        return columns

    def _transform_liquid_limit_data(self, columns: list[str]) -> pd.DataFrame:
        """Transform liquid limit data into a format suitable for analysis.

        This method melts and pivots the DataFrame to organize the liquid limit data by trial,
        including the logarithm of the number of drops for interpolation.

        .. admonition:: **Requires:**
            :class: important

            | :term:`liquid_limit_{n}_drops`
            | :term:`liquid_limit_{n}_moisture_content`

        Parameters
        ----------
        columns: list of str
            A list of column names to include in the transformation.

        Returns
        -------
        :external:class:`~pandas.DataFrame`
            A transformed DataFrame with trial-specific liquid limit data, including a column
            for the logarithm of the number of drops.
        """
        melted_df = pd.melt(
            self._obj[columns],
            id_vars=["point_id", "bottom"],
            value_vars=[col for col in columns if "drops" in col or "moisture_content" in col],
            var_name="variable",
            value_name="value",
        )
        melted_df["type"] = (
            melted_df["variable"].str.extract(r"(drops|moisture_content)").fillna("")
        )
        melted_df["trial_id"] = melted_df["variable"].str.extract(r"(\d+)").astype(int)

        df = melted_df.pivot_table(
            index=["point_id", "bottom", "trial_id"],
            columns="type",
            values="value",
            aggfunc="first",
        ).reset_index()

        df["drops_log"] = np.log(df["drops"])
        df = df.sort_values(["point_id", "bottom", "drops_log"])

        return df

    def get_liquid_limit(self, trials: int = 3) -> pd.Series:
        """Calculate and return the liquid limit according to ASTM D4318 Method A Multipoint Method.

        This method computes the liquid limit by interpolating the moisture content at 25 drops
        using the logarithm of the number of drops and the corresponding moisture content values.

        .. admonition:: **Requires:**
            :class: important

            | :term:`liquid_limit_{n}_drops`
            | :term:`liquid_limit_{n}_moisture_content`

        Parameters
        ----------
        trials: int, default 3
            The number of trials to be considered for interpolation.

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with liquid limit values, calculated by interpolating the moisture content
            at 25 drops.

        References
        ----------
        .. [1] ASTM International. (2018). *Standard test methods for liquid limit, plastic limit,
           and plasticity index of soils* (ASTM D4318-17e1).
           https://doi.org/10.1520/D4318-17E01

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1"],
        ...         "bottom": [1.0],
        ...         "liquid_limit_1_drops": [23],
        ...         "liquid_limit_1_moisture_content": [48.1],
        ...         "liquid_limit_2_drops": [28],
        ...         "liquid_limit_2_moisture_content": [46.7],
        ...         "liquid_limit_3_drops": [33],
        ...         "liquid_limit_3_moisture_content": [46.1],
        ...     }
        ... )
        >>> df.geotech.lab.index.get_liquid_limit(trials=3)
        0    47.539917
        Name: liquid_limit, dtype: Float64
        """
        columns = self._prepare_liquid_limit_data(trials)
        df = self._transform_liquid_limit_data(columns)

        liquid_limit = df.groupby(["point_id", "bottom"]).apply(
            lambda group: _get_linear_forecast(
                group=group,
                x_col_name="drops_log",
                y_col_name="moisture_content",
                x_target=np.log(25),
            ),
            include_groups=False,
        )
        liquid_limit.name = "liquid_limit"
        df = liquid_limit.reset_index()
        df = pd.merge(
            self._obj[["point_id", "bottom"]],
            df,
            on=["point_id", "bottom"],
            how="left",
        )
        liquid_limit = df["liquid_limit"].astype("Float64")

        return liquid_limit

    def get_plastic_limit(self) -> pd.Series:
        """Calculate and return the plastic limit according to ASTM D4318.

        The plastic limit is calculated as the average of two moisture content measurements
        for the plastic limit test.

        .. admonition:: **Requires:**
            :class: important

            | :term:`plastic_limit_1_moisture_content`
            | :term:`plastic_limit_2_moisture_content`

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with plastic limit values.

        References
        ----------
        .. [1] ASTM International. (2018). *Standard test methods for liquid limit, plastic limit,
           and plasticity index of soils* (ASTM D4318-17e1).
           https://doi.org/10.1520/D4318-17E01

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1"],
        ...         "bottom": [1.0],
        ...         "plastic_limit_1_moisture_content": [29.7],
        ...         "plastic_limit_2_moisture_content": [29.1],
        ...     }
        ... )
        >>> df.geotech.lab.index.get_plastic_limit()
        0    29.4
        Name: plastic_limit, dtype: Float64
        """
        self._validate_columns(
            ["plastic_limit_1_moisture_content", "plastic_limit_2_moisture_content"]
        )

        plastic_limit = pd.Series(
            self._obj[
                ["plastic_limit_1_moisture_content", "plastic_limit_2_moisture_content"]
            ].mean(axis=1),
            name="plastic_limit",
        )
        plastic_limit = plastic_limit.astype("Float64")

        return plastic_limit

    def is_nonplastic(self) -> pd.Series:
        """Check if a layer is nonplastic.

        A layer is considered nonplastic if the plastic limit is greater than or equal to the
        liquid limit, or if either the liquid limit or plastic limit are NA.

        .. admonition:: **Requires:**
            :class: important

            | :term:`liquid_limit`
            | :term:`plastic_limit`

        Returns
        -------
        :external:class:`~pandas.Series`
            Boolean series indicating whether each layer is nonplastic.

        References
        ----------
        .. [1] ASTM International. (2018). *Standard test methods for liquid limit, plastic limit,
           and plasticity index of soils* (ASTM D4318-17e1).
           https://doi.org/10.1520/D4318-17E01

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1", "BH-1", "BH-1"],
        ...         "bottom": [1.0, 2.0, 3.0],
        ...         "liquid_limit": [47.5, None, 30.0],
        ...         "plastic_limit": [25.3, 50.0, 50.0],
        ...     }
        ... )
        >>> df.geotech.lab.index.is_nonplastic()
        0    False
        1     True
        2     True
        Name: is_nonplastic, dtype: bool
        """
        self._validate_columns(["liquid_limit", "plastic_limit"])

        liquid_limit = self._obj["liquid_limit"]
        plastic_limit = self._obj["plastic_limit"]
        is_nonplastic = (plastic_limit >= liquid_limit) | liquid_limit.isna() | plastic_limit.isna()
        is_nonplastic.name = "is_nonplastic"

        return is_nonplastic

    def get_plasticity_index(self) -> pd.Series:
        """Calculate and return the plasticity index.

        The plasticity index is calculated as the difference between the liquid limit and the
        plastic limit.

        .. admonition:: **Requires:**
            :class: important

            | :term:`liquid_limit`
            | :term:`plastic_limit`

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with plasticity index values.

        Notes
        -----
        The plasticity index is defined as:

        .. math:: PI = LL - PL

        where:

        - :math:`PI =` plasticity index, %,
        - :math:`LL =` liquid limit, %,
        - :math:`PL =` plastic limit, %.

        References
        ----------
        .. [1] ASTM International. (2018). *Standard test methods for liquid limit, plastic limit,
           and plasticity index of soils* (ASTM D4318-17e1).
           https://doi.org/10.1520/D4318-17E01

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1"],
        ...         "bottom": [1.0],
        ...         "liquid_limit": [47.5],
        ...         "plastic_limit": [25.3],
        ...     }
        ... )
        >>> df.geotech.lab.index.get_plasticity_index()
        0    22.2
        Name: plasticity_index, dtype: Float64
        """
        self._validate_columns(["liquid_limit", "plastic_limit"])

        liquid_limit = self._obj["liquid_limit"]
        plastic_limit = self._obj["plastic_limit"]
        nonplastic_mask = self.is_nonplastic()

        plasticity_index = pd.Series(liquid_limit - plastic_limit, name="plasticity_index")
        plasticity_index[nonplastic_mask] = pd.NA
        plasticity_index = plasticity_index.astype("Float64")

        return plasticity_index

    def get_liquidity_index(self) -> pd.Series:
        r"""Calculate and return the liquidity index.

        The liquidity index is calculated as the ratio of the natural moisture content minus the
        plastic limit to the plasticity index.

        .. admonition:: **Requires:**
            :class: important

            | :term:`moisture_content <{prefix}_moisture_content>`
            | :term:`plastic_limit`
            | :term:`plasticity_index`

        Returns
        -------
        :external:class:`~pandas.Series`
            Series with liquidity index values.

        Notes
        -----
        The liquidity index is defined as:

        .. math:: LI = \frac{w - PL}{PI}

        where:

        - :math:`LI =` liquidity index,
        - :math:`w =` natural moisture content, %,
        - :math:`PL =` plastic limit, %,
        - :math:`PI =` plasticity index, %.

        References
        ----------
        .. [1] ASTM International. (2018). *Standard test methods for liquid limit, plastic limit,
           and plasticity index of soils* (ASTM D4318-17e1).
           https://doi.org/10.1520/D4318-17E01

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "point_id": ["BH-1"],
        ...         "bottom": [1.0],
        ...         "moisture_content": [30.0],
        ...         "plastic_limit": [25.3],
        ...         "plasticity_index": [22.2],
        ...     }
        ... )
        >>> df.geotech.lab.index.get_liquidity_index()
        0    0.211712
        Name: liquidity_index, dtype: Float64
        """
        self._validate_columns(["moisture_content", "plastic_limit", "plasticity_index"])

        moisture_content = self._obj["moisture_content"]
        plastic_limit = self._obj["plastic_limit"]
        plasticity_index = self._obj["plasticity_index"]

        liquidity_index = pd.Series(
            (moisture_content - plastic_limit) / plasticity_index,
            name="liquidity_index",
        )
        liquidity_index = liquidity_index.astype("Float64")

        return liquidity_index
