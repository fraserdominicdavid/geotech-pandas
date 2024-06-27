===============
SPT Subaccessor
===============
In this guide, the basics of the :class:`~pandas.DataFrame.geotech.in_situ.spt` subaccessor methods
are presented. The :class:`~pandas.DataFrame.geotech.in_situ.spt` subaccessor is a collection of
methods related to standard penetration test (SPT) calculations for each sample of each point in the
:external:class:`~pandas.DataFrame`. For information about the columns used by this
subaccessor, see :ref:`spt-columns`.

First, we import the necessary libraries,

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Next, we create a :external:class:`~pandas.DataFrame` with the following data,

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-1", "BH-1", "BH-1", "BH-1", "BH-1"],
            "bottom": [1.0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.0],
            "sample_type": ["spt", "spt", "spt", "spt", "spt", "spt", "spt", "spt"],
            "sample_number": [1, 2, 3, 4, 5, 6, 7, 8],
            "blows_1": [0, 10, 14, 18, 25, 33, 40, 50],
            "blows_2": [0, 12, 13, 20, 29, 35, 45, None],
            "blows_3": [0, 15, 13, 23, 27, 37, 50, None],
            "pen_1": [150, 150, 150, 150, 150, 150, 150, 10],
            "pen_2": [150, 150, 150, 150, 150, 150, 150, None],
            "pen_3": [150, 150, 150, 150, 150, 150, 50, None],
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

Checking for refusal samples
----------------------------
It is possible to check for which samples refused penetration through
:meth:`~pandas.DataFrame.geotech.in_situ.spt.is_refusal`. This method will return ``True`` for any
sample that may be considered a refusal.

A sample is considered a refusal when any of the following is true:

- a total of 50 blows or more have been applied during any of the three 150 mm increments;
- a total of 100 blows or more have been applied; and
- partial penetration, which signifies that the sampler can no longer penetrate through the
  strata, is present in any of the increments.

.. ipython:: python

    df.geotech.in_situ.spt.is_refusal()

Checking for hammer weight samples
----------------------------------
It is also possible to check which samples are hammer weights through
:meth:`~pandas.DataFrame.geotech.in_situ.spt.is_hammer_weight`. This method will return ``True`` for
any sample that may be considered hammer weight.

A sample is considered hammer weight when all of the following are true:

- a total of 450 mm or more was penetrated by the sampler through sinking; and
- each 150 mm increment has 0 blows recorded.

This can be defined in a :external:class:`~pandas.DataFrame` similar to how the first sample is
recorded. The blow counts and penetration measurements for all three increments are ``0`` and
``150``, respectively.

.. ipython:: python

    df.geotech.in_situ.spt.is_hammer_weight()

Getting the N-value
-------------------
The SPT is mainly done to calculate the N-value. This can easily be calculated using the
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_n_value` method for each sample/layer.

.. ipython:: python

    df.geotech.in_situ.spt.get_n_value()

As you can see, the N-values for the last three samples are set to 50, but why? This is because
these samples are refusals and are assumed to have an N-value of 50; however, this behavior can be
customized.

Setting the assumed refusal N-value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The assumed refusal N-value can easily be changed by setting the ``refusal`` parameter like so,

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

As you can see, the N-value at index ``4`` was limited from 56 to 50.

.. warning::

    Setting ``limit`` to ``True`` while also setting ``refusal`` to :external:attr:`~pandas.NA` will
    have a similar output to ``Out[16]`` above. That is to say, the refusal N-value will change as
    expected, however, since it is essentially nothing, nothing will get limited as well.

    .. ipython:: python
        :okwarning:

        df.geotech.in_situ.spt.get_n_value(refusal=pd.NA, limit=True)
    
    Don't worry if you forget about this warning, since geotech-pandas will warn you when it detects
    you using such settings.

Getting a simple SPT report
---------------------------
A simple descriptive report of the blow counts and the N-value can be obtained through the
:meth:`~pandas.DataFrame.geotech.in_situ.spt.get_report` method,

.. ipython:: python

    df.geotech.in_situ.spt.get_report()
