======
Basics
======
geotech-pandas is mainly accessed from the :class:`~pandas.DataFrame.geotech` accessor on
:external:class:`~pandas.DataFrame` objects. When accessed, geotech-pandas validates the current
:external:class:`~pandas.DataFrame` for several minimum requirements. These requirements are
discussed in the following sections.

Customarily, we import the necessary libraries before we begin the guide,

.. ipython:: python

    import pandas as pd
    import geotech_pandas

Minimum requirements
--------------------
Columns
^^^^^^^
The minimum required columns for geotech-pandas are the ``point_id`` and ``bottom`` columns. The
``point_id`` represents the ID or the group where each layer belongs to. Whereas, the ``bottom``
column represents the bottom depths of these layers. For more information, see
:ref:`general-columns`.

If you try to access :class:`~pandas.DataFrame.geotech` with the following
:external:class:`~pandas.DataFrame`,

.. ipython:: python
    :okexcept:

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
        }
    )
    df.geotech()

An :external:class:`AttributeError` is raised stating that the :external:class:`~pandas.DataFrame`
is missing the ``bottom`` column.

Arrangement
^^^^^^^^^^^
Another requirement is that the ``bottom`` depth values for each ``point_id`` should be
monotonically increasing, as most methods assume that each layer comes right after the other in each
point.

If you try to access :class:`~pandas.DataFrame.geotech` with the following
:external:class:`~pandas.DataFrame`,

.. ipython:: python
    :okexcept:

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [0.0, 2.0, 1.0],
        }
    )
    df.geotech()

An :external:class:`AttributeError` is raised listing which points contain the erroneous
arrangement.

Uniqueness
^^^^^^^^^^
It is also required that the ``point_id`` and ``bottom`` pairs to be unique, as most methods
assume that each layer is unique for each point.

If you try to access :class:`~pandas.DataFrame.geotech` with the following
:external:class:`~pandas.DataFrame`,

.. ipython:: python
    :okexcept:

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [0.0, 1.0, 1.0],
        }
    )
    df.geotech()

An :external:class:`AttributeError` is raised listing which points contain duplicate values.

Subaccessors
------------
There are no available methods under the :class:`~pandas.DataFrame.geotech` accessor other than the
validation methods that are called automatically upon initiation of the accessor as shown in the
preceding sections.

The :class:`~pandas.DataFrame.geotech` accessor serves as a parent namespace to the various scopes
provided in geotech-pandas. These scopes are accessors that can be accessed from
:class:`~pandas.DataFrame.geotech` like so,

.. ipython:: python

    df = pd.DataFrame(
        {
            "point_id": ["BH-1", "BH-1", "BH-1"],
            "bottom": [0.0, 1.0, 2.0],
        }
    )
    df.geotech.point

Here, we can access the :class:`~pandas.DataFrame.geotech.point` accessor where point-related
methods can be accessed. Suceeding guides demonstrate the usage of each subaccessor in
geotech-pandas.
