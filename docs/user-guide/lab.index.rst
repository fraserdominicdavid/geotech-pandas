======================
Soil Index Subaccessor
======================
In this guide, the basics of the :class:`~pandas.DataFrame.geotech.lab.index` subaccessor methods
are presented. The :class:`~pandas.DataFrame.geotech.lab.index` subaccessor is a collection of
methods related to index property laboratory tests for each sample of each point in the
:external:class:`~pandas.DataFrame`. The index properties of soil are the properties which help to
assess the engineering behavior of soil and determine the classification of soil accurately. For
information about the columns used by this subaccessor, see :ref:`soil-index-columns`.

First, we import the necessary libraries,

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Next, we create a :external:class:`~pandas.DataFrame` with the following data,

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-1"],
            "bottom": [1.0, 1.5, 3.0, 4.5],
            "moisture_content_mass_moist": [236.44, 154.40, 164.68, 135.61],
            "moisture_content_mass_dry": [174.40, 120.05, 134.31, 107.64],
            "moisture_content_mass_container": [22.20, 18.66, 20.27, 22.32],
            "liquid_limit_1_drops": [19, 18, 20, pd.NA],
            "liquid_limit_1_mass_moist": [13.91, 14.58, 16.24, pd.NA],
            "liquid_limit_1_mass_dry": [10.56, 11.23, 12.56, pd.NA],
            "liquid_limit_1_mass_container": [3.22, 3.28, 3.24, pd.NA],
            "liquid_limit_2_drops": [25, 25, 26, pd.NA],
            "liquid_limit_2_mass_moist": [18.48, 13.36, 12.23, pd.NA],
            "liquid_limit_2_mass_dry": [13.78, 10.45, 9.74, pd.NA],
            "liquid_limit_2_mass_container": [3.15, 3.27, 3.26, pd.NA],
            "liquid_limit_3_drops": [31, 32, 35, pd.NA],
            "liquid_limit_3_mass_moist": [21.38, 17.77, 13.40, pd.NA],
            "liquid_limit_3_mass_dry": [15.91, 13.67, 10.64, pd.NA],
            "liquid_limit_3_mass_container": [3.21, 3.24, 3.23, pd.NA],
            "plastic_limit_1_mass_moist": [12.26, 11.66, 13.22, pd.NA],
            "plastic_limit_1_mass_dry": [10.23, 9.89, 11.28, pd.NA],
            "plastic_limit_1_mass_container": [2.57, 2.99, 2.97, pd.NA],
            "plastic_limit_2_mass_moist": [11.17, 13.20, 17.01, pd.NA],
            "plastic_limit_2_mass_dry": [9.45, 11.01, 14.30, pd.NA],
            "plastic_limit_2_mass_container": [3.07, 2.56, 2.90, pd.NA],
        }
    )
    df = df.convert_dtypes()
    df

.. note::

    Notice that the ``df`` is reassigned with the result of
    :external:meth:`~pandas.DataFrame.convert_dtypes` method. This method converts the columns of
    ``df`` to the best possible dtypes that support :external:attr:`~pandas.NA` to consistently
    represent missing data.

    Use the :external:attr:`~pandas.DataFrame.dtypes` property to show the current dtypes of ``df``,

    .. ipython:: python

        df.dtypes

Getting the moisture content
----------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.get_moisture_content` method returns a
:external:class:`~pandas.Series` of moisture content values. This method requires the following
columns:

- :term:`moisture_content_mass_moist <{prefix}_mass_moist>`: mass of container and
  moist specimen, g.
- :term:`moisture_content_mass_dry <{prefix}_mass_dry>`: mass of container and oven
  dry specimen, g.
- :term:`moisture_content_mass_container <{prefix}_mass_container>`: mass of
  container, g.

.. note::

    Since the result of this method is in the form of a percentage, it isn't particularly strict in
    using `g` as the unit. However, it is still important to use a consistent unit across these
    columns.

.. ipython:: python

    df["moisture_content"] = df.geotech.lab.index.get_moisture_content()
    df["moisture_content"]

Getting the liquid limit
------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.get_liquid_limit` method calculates and returns the
liquid limit according to ASTM D4318 Method A Multipoint Method. The method interpolates the
moisture content at 25 drops using the logarithm of the number of drops and the corresponding
moisture content values. For 3 trials, this method requires the following columns:

- :term:`liquid_limit_1_drops <liquid_limit_{n}_drops>`: number of drops causing closure of the
  groove for trial 1, drops.
- :term:`liquid_limit_1_moisture_content <liquid_limit_{n}_moisture_content>`: moisture content for
  trial 1, %.
- :term:`liquid_limit_2_drops <liquid_limit_{n}_drops>`: number of drops causing closure of the
  groove for trial 2, drops.
- :term:`liquid_limit_2_moisture_content <liquid_limit_{n}_moisture_content>`: moisture content for
  trial 2, %.
- :term:`liquid_limit_3_drops <liquid_limit_{n}_drops>`: number of drops causing closure of the
  groove for trial 3, drops.
- :term:`liquid_limit_3_moisture_content <liquid_limit_{n}_moisture_content>`: moisture content for
  trial 3, %.

Since there are no moisture content columns for each trial, we can use the
:meth:`~pandas.DataFrame.geotech.lab.index.get_moisture_content` method to calculate
the moisture content for each trial and assign it back to the dataframe.

.. ipython:: python

    df["liquid_limit_1_moisture_content"] = df.geotech.lab.index.get_moisture_content(prefix="liquid_limit_1")
    df["liquid_limit_1_moisture_content"]
    df["liquid_limit_2_moisture_content"] = df.geotech.lab.index.get_moisture_content(prefix="liquid_limit_2")
    df["liquid_limit_2_moisture_content"]
    df["liquid_limit_3_moisture_content"] = df.geotech.lab.index.get_moisture_content(prefix="liquid_limit_3")
    df["liquid_limit_3_moisture_content"]

Now that all required columns are present, we can call the
:meth:`~pandas.DataFrame.geotech.lab.index.get_liquid_limit` method to calculate the liquid limit
for each sample in the dataframe.

.. ipython:: python

    df["liquid_limit"] = df.geotech.lab.index.get_liquid_limit()
    df["liquid_limit"]

Getting the plastic limit
-------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.get_plastic_limit` method calculates and returns 
the plastic limit according to ASTM D4318. The plastic limit is the average of two moisture 
content measurements for the plastic limit test. This method requires the following columns:

- :term:`plastic_limit_1_moisture_content`: moisture content for the first plastic limit test, %.
- :term:`plastic_limit_2_moisture_content`: moisture content for the second plastic limit test, %.

Since there are no moisture content columns for each test, we can use the
:meth:`~pandas.DataFrame.geotech.lab.index.get_moisture_content` method to calculate
the moisture content for each test and assign it back to the dataframe.

.. ipython:: python

    df["plastic_limit_1_moisture_content"] = df.geotech.lab.index.get_moisture_content(prefix="plastic_limit_1")
    df["plastic_limit_1_moisture_content"]
    df["plastic_limit_2_moisture_content"] = df.geotech.lab.index.get_moisture_content(prefix="plastic_limit_2")
    df["plastic_limit_2_moisture_content"]

Now that all required columns are present, we can call the
:meth:`~pandas.DataFrame.geotech.lab.index.get_plastic_limit` method to calculate the plastic limit
for each sample in the dataframe.

.. ipython:: python

    df["plastic_limit"] = df.geotech.lab.index.get_plastic_limit()
    df["plastic_limit"]

Checking for nonplastic layers
------------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.is_nonplastic` method checks if a layer is
nonplastic. A layer is considered nonplastic if the plastic limit is greater than or equal to the
liquid limit, or if either the liquid limit or plastic limit is missing
(:external:attr:`~pandas.NA`). This method requires the following columns:

- :term:`liquid_limit`: liquid limit, %.
- :term:`plastic_limit`: plastic limit, %.

.. ipython:: python

    df.geotech.lab.index.is_nonplastic()

Getting the plasticity index
----------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.get_plasticity_index` method calculates the
plasticity index as the difference between the liquid limit and the plastic limit. If a layer is
nonplastic, the plasticity index is set to :external:attr:`~pandas.NA`. This method requires the
following columns:

- :term:`liquid_limit`: liquid limit, %.
- :term:`plastic_limit`: plastic limit, %.

.. ipython:: python

    df["plasticity_index"] = df.geotech.lab.index.get_plasticity_index()
    df["plasticity_index"]

Getting the liquidity index
----------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.get_liquidity_index` method calculates the liquidity
index as the ratio of the natural moisture content minus the plastic limit to the plasticity index.
This method requires the following columns:

- :term:`moisture_content <{prefix}_moisture_content>`: moisture content, %.
- :term:`plastic_limit`: plastic limit, %.
- :term:`plasticity_index`: plasticity index, %.

.. ipython:: python

    df["liquidity_index"] = df.geotech.lab.index.get_liquidity_index()
    df["liquidity_index"]
