"""Subaccessor that contains methods related to index property tests."""

import pandas as pd

from geotech_pandas.base import GeotechPandasBase


class IndexDataFrameAccessor(GeotechPandasBase):
    """Subaccessor that contains methods related to index property tests.

    The index properties of soil are the properties which help to assess the engineering behavior of
    soil and determine the classification of soil accurately. Some key properties include:

    - moisture content
    - particle size distribution
    - consistency or Atterberg limits
    - specific gravity
    """

    def get_moisture_content(self, prefix="moisture_content") -> pd.Series:
        r"""Return moisture content calculation according to ASTM D2216.

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
