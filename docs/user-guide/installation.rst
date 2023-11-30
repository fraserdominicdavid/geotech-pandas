============
Installation
============
There are a lot of ways to install Python packages, however, it is important to ensure reproducible
installs. The best practice is to:

#. use a different environment per project; and
#. record dependency versions using your preferred package installer.

For this guide, we will be using `Poetry <https://python-poetry.org/>`__ for its dependency resolver
and isolation capabilites that agree well with the said best practices. For more information on
how to get started with Poetry, see `Basic usage <https://python-poetry.org/docs/basic-usage/>`__.

Once you're done setting up, add and install this package as a dependency of your project using::

    poetry add geotech-pandas

From here on, you can proceed with developing your project using
`Jupyter notebooks <https://jupyter.org/>`__ for exploratory and interactive computing, or IDEs such
as `Visual Studio Code <https://code.visualstudio.com/>`__ for writing scripts and packages.
