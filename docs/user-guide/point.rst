=================
Point Subaccessor
=================
In this guide, the basics of the :class:`~pandas.DataFrame.geotech.point` subaccessor methods are
presented. The :class:`~pandas.DataFrame.geotech.point` subaccessor is a collection of depth-related
calculations for each point in the :external:class:`~pandas.DataFrame` differentiated by their
``point_id``.

First, we import the necessary libraries.

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Next, we create a simple :external:class:`~pandas.DataFrame` with ``point_id`` and ``bottom``
columns present. The ``point_id`` represents the ID or the group where each layer is in, whereas the
``bottom`` column represents the bottom depths of each layer. An additional ``soil_type`` column is
also added to show how this column is transformed when :ref:`splitting <splitting-layers>`.

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [1.0, 2.0, 3.0],
            "soil_type": ["sand", "clay", "sand"],
        }
    )
    df

Getting layer top depth data
----------------------------
One of the methods under :class:`~pandas.DataFrame.geotech.point` is the ability to get the top
depths of each layer based on their bottom depths. The
:meth:`~pandas.DataFrame.geotech.point.get_top` method returns a :external:class:`~pandas.Series`
that represents the top depths based on the bottom depths of each layer.

.. ipython:: python

    df.geotech.point.get_top()

Assign the results of :meth:`~pandas.DataFrame.geotech.point.get_top` to a column in the
:external:class:`~pandas.DataFrame` to store the results. It is recommended to assign the results in
a column with the same name as the :external:class:`~pandas.Series` name returned by the
:meth:`~pandas.DataFrame.geotech.point.get_top` method.

.. ipython:: python

    df["top"] = df.geotech.point.get_top()
    df

To avoid manually setting the column name, we can utilize the :external:func:`~pandas.concat` method
since this method sets the :external:class:`~pandas.Series` name as the column name when
concatenating a :external:class:`~pandas.DataFrame` with a :external:class:`~pandas.Series`.

To demonstrate this, we must delete the column we created earlier first.

.. ipython:: python

    del df["top"]
    df

Then proceed with the following command to concatenate ``df`` with the results of
:meth:`~pandas.DataFrame.geotech.point.get_top`.

.. ipython:: python

    df = pd.concat((df, df.geotech.point.get_top()), axis=1)
    df

As you can see, it results to the same :external:class:`~pandas.DataFrame` as before.

It is recommended to use the :external:func:`~pandas.concat` method since :mod:`geotech-pandas`
relies heavily in consistent :ref:`column names <columns>`.

If you want the output to be much cleaner, you can always override the arrangement of columns like
so,

.. ipython:: python

    df = df[["point_id", "top", "bottom", "soil_type"]]
    df

Getting layer center data
-------------------------
The :meth:`~pandas.DataFrame.geotech.point.get_center` method returns the center depth of each layer
based on the average of the ``top`` and ``bottom`` columns.

.. ipython:: python

    df.geotech.point.get_center()

Similar to before, we can store the results using :external:func:`~pandas.concat`.

.. ipython:: python

    df = pd.concat((df, df.geotech.point.get_center()), axis=1)
    df

Moving ``soil_type`` to the end,

.. ipython:: python

    col = df.pop("soil_type")
    df.insert(len(df.columns), col.name, col)
    df

Getting layer thickness data
----------------------------
The :meth:`~pandas.DataFrame.geotech.point.get_thickness` method returns the thickness of each layer
in terms of depth of each layer by getting the absolute difference between the ``top`` and
``bottom`` columns.

.. ipython:: python

    df.geotech.point.get_thickness()

Similar to before, we can store the results using :external:func:`~pandas.concat`.

.. ipython:: python

    df = pd.concat((df, df.geotech.point.get_thickness()), axis=1)
    df

Since we already stored ``soil_type`` in ``col`` earlier and no changes occurred to ``soil_type``
since then, we can simply delete ``soil_type`` from ``df`` and re-insert ``col`` at the end of 
``df`` like so,

.. ipython:: python

    del df[col.name]
    df.insert(len(df.columns), col.name, col)
    df

.. _splitting-layers:

Splitting layers
----------------
The :meth:`~pandas.DataFrame.geotech.point.split_at_depth` method returns a
:external:class:`~pandas.DataFrame` where each layer is split into two if the provided depth is
found within its ``top`` and ``bottom`` depths.

For example, if wish to split *BH-1* at 1.5 m, we call
:meth:`~pandas.DataFrame.geotech.point.split_at_depth` with the ``depth`` argument as ``1.5``.

.. ipython:: python

    df = df.geotech.point.split_at_depth(depth=1.5)
    df

As you can see, the :external:class:`~pandas.DataFrame` has been split and the ``top`` and
``bottom`` columns have been updated correctly. However, the other depth-related data remain the
same when they should also be different. At the moment, this is the limitation of
:meth:`~pandas.DataFrame.geotech.point.split_at_depth` as it only updates the ``top`` and ``bottom``
columns. There are workarounds to this issue though. You can either reassign the other depth-related
columns or split the :external:class:`~pandas.DataFrame` first before performing depth related
calculations.

Fortunately, :external:mod:`pandas` offers the :external:meth:`~pandas.DataFrame.update` method for
:external:class:`~pandas.DataFrame` objects. As such, we can update and correct the
:external:class:`~pandas.DataFrame` using the following commands.

.. ipython:: python

    df.update(df.geotech.point.get_center())
    df.update(df.geotech.point.get_thickness())
    df

Note that :external:meth:`~pandas.DataFrame.update` transforms the
:external:class:`~pandas.DataFrame` inplace.
