=================
Point Subaccessor
=================
In geotech-pandas, a **point** represents the point in which a borehole or a soil profile is
located.

In this guide, the basics of the :class:`~pandas.DataFrame.geotech.point` subaccessor methods are
presented. The :class:`~pandas.DataFrame.geotech.point` subaccessor is a collection of point-related
methods intended for managing points in a :external:class:`~pandas.DataFrame` that contains one or
more points.

First, we import the necessary libraries,

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Next, we create a simple :external:class:`~pandas.DataFrame` with the following data,

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1", "BH-2", "BH-2"],
            "top": [0.0, 1.0, 2.0, 0.0, 1.0],
            "bottom": [1.0, 2.0, 3.0, 1.0, 5.0],
            "soil_type": ["sand", "clay", "sand", "sand", "clay"],
        }
    )
    df

Getting a specific point
------------------------
The :meth:`~pandas.DataFrame.geotech.point.get_group` method returns a copy of the supplied
``point_id``.

If you somehow forgot the IDs we stored in ``df`` earlier, then you can easliy check the list stored
in the :attr:`~pandas.DataFrame.geotech.point.ids` attribute,

.. ipython:: python

    df.geotech.point.ids

Now, if you wish to get a copy of **BH-1**,

.. ipython:: python

    df.geotech.point.get_group("BH-1")

On the other hand, getting a copy of **BH-2**,

.. ipython:: python

    df.geotech.point.get_group("BH-2")

.. note::

    :meth:`~pandas.DataFrame.geotech.point.get_group` only returns copies of the sliced
    :external:class:`~pandas.DataFrame`, so modifying it will not change anything in the original
    :external:class:`~pandas.DataFrame`.

    For example, if we modify the soil type of **BH-2** to rock,

    .. ipython:: python

        bh2 = df.geotech.point.get_group("BH-2")
        bh2.loc[:, "soil_type"] = "rock"
        bh2

    Then get a new copy of **BH-2** from ``df``,

    .. ipython:: python

        df.geotech.point.get_group("BH-2")
    
    As you can see, the :external:class:`~pandas.DataFrame` copy in ``bh2`` was modified, but not
    the new copy from the source :external:class:`~pandas.DataFrame`. This is because of the
    Copy-on-Write optimizations in :external:mod:`pandas` which prevents modifications on copies to
    reflect on the source. Keep this in mind when modifying copies as it may not be the behavior you
    want. For more information, see `Copy-on-Write (CoW)
    <https://pandas.pydata.org/docs/user_guide/copy_on_write.html>`__.
