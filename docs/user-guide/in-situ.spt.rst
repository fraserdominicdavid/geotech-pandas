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

Getting the seating penetration
-------------------------------
The :meth:`~pandas.DataFrame.geotech.in_situ.spt.get_seating_pen` method returns a
:external:class:`~pandas.Series` of penetration measurements in the first increment, where the
measurements are exactly 150 mm. Measurements that do not meet the requirements are
masked with :external:attr:`~pandas.NA`.

.. ipython:: python

    df.geotech.in_situ.spt.get_seating_pen()

Getting the main penetration
----------------------------
The :meth:`~pandas.DataFrame.geotech.in_situ.spt.get_main_pen` method returns a
:external:class:`~pandas.Series` with the sum of the penetration in the second and third 150 mm
increment for each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_main_pen()

Getting the total penetration
-----------------------------
One of the methods under :class:`~pandas.DataFrame.geotech.in_situ.spt` is the ability to get the
total penetration of each SPT increment. The
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_total_pen` method returns a
:external:class:`~pandas.Series` with the sum of the penetration per inteval in each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_total_pen()

Getting the seating drive
-------------------------
It is also possible to get the seating drive, which is, by definition, the number of blows required
to penetrate the first 150 mm increment. The
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_seating_drive` method returns such a result for
each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_seating_drive()

.. note::

    Notice that the last value is :external:attr:`~pandas.NA`, this is because the first increment
    didn't reach the full 150 mm requirement. Such cases are usually considered as invalid tests or
    hint to the start of a hard layer of soil or rock.

Getting the main drive
----------------------
The main drive, which is the total number of blows in the second and third 150 mm increment, can
also be returned by the :meth:`~pandas.DataFrame.geotech.in_situ.spt.get_main_drive` method for each
sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_main_drive()

.. note::

    This method simply sums up the second and third increment regardless if the increments are
    completely penetrated or not. Due to this, the main drive may not always correspond to the
    reported N-value.

Getting the total drive
-----------------------
It is also possible to calculate the total number of blows in all three 150 mm increments for each
sample/layer through the :meth:`~pandas.DataFrame.geotech.in_situ.spt.get_total_drive` method.

.. ipython:: python

    df.geotech.in_situ.spt.get_total_drive()

Getting the N-value
-------------------
The SPT is mainly done to calculate the N-value. This can easily be calculated using the
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_n_value` method for each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_n_value()

As you can see, the N-value for the last two samples are set to 50, but why? This is because the
total penetration in these samples are less than 450 mm. This means that these samples satisfy the
refusal criteria and are assumed to have an N-value of 50.

Setting the assumed refusal N-value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The refusal N-value can easily be changed by setting the ``refusal`` parameter like so,

.. ipython:: python

    df.geotech.in_situ.spt.get_n_value(refusal=100)

You can also set it to :external:attr:`~pandas.NA` if you don't want to assume a refusal N-value,

.. ipython:: python

    df.geotech.in_situ.spt.get_n_value(refusal=pd.NA)

Limiting the N-values
^^^^^^^^^^^^^^^^^^^^^
The ``limit`` parameter is also available if you wish to limit the non-refusal N-values to the
refusal N-value. To limit the N-values, just set the ``limit`` parameter to ``True``,

.. ipython:: python

    df.geotech.in_situ.spt.get_n_value(limit=True)

As you can see, the N-value in index ``4`` was limited from 72 to 50.

.. warning::

    Setting ``limit`` to ``True`` while also setting ``refusal`` to :external:attr:`~pandas.NA` will
    have a similar output to ``Out[15]`` above. That is to say, the refusal N-value will change as
    expected, however, since it is essentially nothing, nothing will get limited as well.

    .. ipython:: python
        :okwarning:

        df.geotech.in_situ.spt.get_n_value(refusal=pd.NA, limit=True)
    
    :mod:`geotech-pandas` will warn you if it detects you using such settings, so don't worry if you
    forget about this warning.
