==========
User Guide
==========

The user guide covers all of geotech-pandas by topic area. Each of the subsections introduces a
topic, and discusses how geotech-pandas approaches the problem, with many
examples throughout.

The methods in geotech-pandas are designed to work on multiple points at the same time which
effectively reduces the time required for routine tasks. However, most guides are demonstrated with
:external:class:`~pandas.DataFrame` objects with only one point for brevity.

.. note::
    
    In geotech-pandas, a **point** represents the point in which a borehole or a soil profile is
    located. For now, geotech-pandas is location-unaware so it is not required to supply geographic
    data in :external:class:`~pandas.DataFrame` objects. This may change in the future to support
    methods for plotting site maps and similar tasks.

Further information on any specific method can be obtained in the :doc:`../api-reference/index`.

If you're new to `Pandas <https://pandas.pydata.org/>`__ in general, it is recommended to make
yourself familiar with it first by heading to the
`Pandas documentation <https://pandas.pydata.org/docs/>`__.

How to read these guides
------------------------

In these guides, you will see input code inside code blocks such as,

::

    import pandas as pd
    import geotech_pandas
    pd.DataFrame({'A': [1, 2, 3]})


or,

.. ipython:: python

    import pandas as pd
    import geotech_pandas
    pd.DataFrame({'A': [1, 2, 3]})

The first block is a standard python input, while in the second block, the ``In [x]:`` indicates
that the input is inside a `Jupyter notebook <https://jupyter.org>`__ where ``x`` is the line
number. In Jupyter notebooks, the last line is printed and plots are shown inline indicated by
``Out[x]:``.

For example,

.. ipython:: python

    a = 1
    a

is equivalent to,

::

    a = 1
    print(a)

Guides
------

.. toctree::
    :caption: Getting Started
    :maxdepth: 2

    introduction
    installation

.. toctree::
    :caption: Usage and Subaccessors
    :maxdepth: 2

    basics
    point
    layer
    in-situ
    lab
