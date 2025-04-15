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
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [1.0, 1.5, 3.0],
            "moisture_content_mass_moist": [236.44, 154.40, 164.68],
            "moisture_content_mass_dry": [174.40, 120.05, 134.31],
            "moisture_content_mass_container": [22.20, 18.66, 20.27],
            "liquid_limit_1_drops": [19, 18, 20],
            "liquid_limit_1_mass_moist": [13.91, 14.58, 16.24],
            "liquid_limit_1_mass_dry": [10.56, 11.23, 12.56],
            "liquid_limit_1_mass_container": [3.22, 3.28, 3.24],
            "liquid_limit_2_drops": [25, 25, 26],
            "liquid_limit_2_mass_moist": [18.48, 13.36, 12.23],
            "liquid_limit_2_mass_dry": [13.78, 10.45, 9.74],
            "liquid_limit_2_mass_container": [3.15, 3.27, 3.26],
            "liquid_limit_3_drops": [31, 32, 35],
            "liquid_limit_3_mass_moist": [21.38, 17.77, 13.40],
            "liquid_limit_3_mass_dry": [15.91, 13.67, 10.64],
            "liquid_limit_3_mass_container": [3.21, 3.24, 3.23],
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

- ``moisture_content_mass_moist``: mass of container and moist specimen, g.
- ``moisture_content_mass_dry``: mass of container and oven dry specimen, g.
- ``moisture_content_mass_container``: mass of container, g.

.. note::

    Since the result of this method is in the form of a percentage, it isn't particularly strict in
    using `g` as the unit. However, it is still important to use a consistent unit across these
    columns.

.. ipython:: python

    df.geotech.lab.index.get_moisture_content()

Getting the liquid limit
------------------------
The :meth:`~pandas.DataFrame.geotech.lab.index.get_liquid_limit` method calculates and returns the
liquid limit according to ASTM D4318 Method A Multipoint Method. The method interpolates the
moisture content at 25 drops using the logarithm of the number of drops and the corresponding
moisture content values. For 3 trials, this method requires the following columns:

- ``liquid_limit_1_drops``: number of drops causing closure of the groove for trial 1, drops.
- ``liquid_limit_1_moisture_content``: moisture content for trial 1, %.
- ``liquid_limit_2_drops``: number of drops causing closure of the groove for trial 2, drops.
- ``liquid_limit_2_moisture_content``: moisture content for trial 2, %.
- ``liquid_limit_3_drops``: number of drops causing closure of the groove for trial 3, drops.
- ``liquid_limit_3_moisture_content``: moisture content for trial 3, %.

Since, there are no moisture content columns for each trial, we can use the
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

    df.geotech.lab.index.get_liquid_limit()
