===============
SPT Subaccessor
===============
In this guide, the basics of the :class:`~pandas.DataFrame.geotech.in_situ.spt` subaccessor methods
are presented. The :class:`~pandas.DataFrame.geotech.in_situ.spt` subaccessor is a collection of
methods related to standard penetration test (SPT) calculations for each sample of each point in the
:external:class:`~pandas.DataFrame`.

First, we import the necessary libraries,

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Next, we create a :external:class:`~pandas.DataFrame` with the following data,

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-1", "BH-1", "BH-1", "BH-1"],
            "bottom": [1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.0],
            "sample_type": ["spt", "spt", "spt", "spt", "spt", "spt", "spt"],
            "sample_number": [1, 2, 3, 4, 5, 6, 7],
            "blows_1": [10, 14, 18, 25, 33, 40, 50],
            "blows_2": [12, 13, 20, 20, 35, 45, None],
            "blows_3": [15, 13, 23, 27, 37, 50, None],
            "pen_1": [150, 150, 150, 150, 150, 150, 10],
            "pen_2": [150, 150, 150, 150, 150, 150, None],
            "pen_3": [150, 150, 150, 150, 150, 50, None],
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

Getting the total penetration
-----------------------------
One of the methods under :class:`~pandas.DataFrame.geotech.in_situ.spt` is the ability to get the
total penetration of each SPT interval. The
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_total_pen` method returns a
:external:class:`~pandas.Series` with the sum of the penetration per inteval in each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_total_pen()

Getting the seating drive
-------------------------
It is also possible to get the seating drive, which is, by definition, the number of blows required
to penetrate the first 150 mm interval. The
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_seating_drive` method returns such a result for
each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_seating_drive()

.. note::

    Notice that the last value is :external:attr:`~pandas.NA`, this is because the first interval
    didn't reach the full 150 mm requirement. Such cases are usually considered as invalid tests or
    hint to the start of a hard layer of soil or rock.
