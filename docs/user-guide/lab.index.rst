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
