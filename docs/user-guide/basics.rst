.. _basics:

======
Basics
======
:mod:`geotech-pandas` is mainly accessed from the :py:class:`~pandas.DataFrame.geotech` accessor on
:external:py:class:`~pandas.DataFrame` objects. When accessed, :mod:`geotech-pandas`
validates the current :external:py:class:`~pandas.DataFrame` for several minimum
requirements. These requirements are discussed in the following sections.

Customarily, we import as follows before we begin the guide,

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Required Columns
----------------
The minimum required columns for :mod:`geotech-pandas` are the ``point_id`` and ``bottom`` columns.
The ``point_id`` represents the ID or the group where each observation or soil layer belongs to.
Whereas, the ``bottom`` column represents the bottom depths of these observations.

If you try to access :py:class:`~pandas.DataFrame.geotech` with the following
:external:py:class:`~pandas.DataFrame`,

.. ipython:: python
    :okexcept:

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
        }
    )
    df.geotech()

An :external:py:class:`AttributeError` is raised stating that the
:external:py:class:`~pandas.DataFrame` is missing the ``bottom`` column.

Required Arrangement
--------------------
:mod:`geotech-pandas` requires that the ``bottom`` depth values for each ``point_id`` are
monotonically increasing, as most methods assume that each layer comes right after the other in each
point.

If you try to access :py:class:`~pandas.DataFrame.geotech` with the following
:external:py:class:`~pandas.DataFrame`,

.. ipython:: python
    :okexcept:

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [0.0, 2.0, 1.0],
        }
    )
    df.geotech()

An :external:py:class:`AttributeError` is raised listing which points contain the erroneous
arrangement.

Required Uniqueness
-------------------
:mod:`geotech-pandas` requires ``point_id`` and ``bottom`` pairs to be unique, as most methods
assume that each layer is unique for each point.

If you try to access :py:class:`~pandas.DataFrame.geotech` with the following
:external:py:class:`~pandas.DataFrame`,

.. ipython:: python
    :okexcept:

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [0.0, 1.0, 1.0],
        }
    )
    df.geotech()

An :external:py:class:`AttributeError` is raised listing which points contain duplicate values.

Subaccessors
------------
There are no available methods under the :py:class:`~pandas.DataFrame.geotech` accessor other than
the validation methods that are called automatically upon initiation of the accessor as shown in the
preceding sections.

The :py:class:`~pandas.DataFrame.geotech` accessor serves as a parent namespace to the various
scopes provided in :mod:`geotech-pandas`. These scopes are accessors that can be accessed from
:py:class:`~pandas.DataFrame.geotech` like so,

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [0.0, 1.0, 2.0],
        }
    )
    df.geotech.point

Here, we can access the :py:class:`~pandas.DataFrame.geotech.point` accessor where depth-related
calculations can be accessed. Head to the related :doc:`guide <point>` for more information about
the :py:class:`~pandas.DataFrame.geotech.point` accessor.
