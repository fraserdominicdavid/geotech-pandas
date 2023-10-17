.. _user_guide:

==========
User Guide
==========

The user guide covers all of :mod:`geotech-pandas` by topic area. Each of the subsections
introduces a topic, and discusses how :mod:`geotech-pandas` approaches the problem, with many
examples throughout.

Further information on any specific method can be obtained in the :ref:`api_reference`.

If you're new to `pandas <https://pandas.pydata.org/>`__ in general, it is recommended to make
yourself familiar with it first by heading to the
`pandas documentation <https://pandas.pydata.org/docs/>`__.

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
    :caption: Usage and Accessors
    :maxdepth: 2

    basics
    point
