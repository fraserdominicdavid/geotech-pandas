.. currentmodule:: pandas

=============
API Reference
=============

:mod:`geotech-pandas` provides scope-specific methods under various subaccessors. These are separate
namespaces within :class:`~pandas.DataFrame.geotech`.

.. autoaccessorcallable:: DataFrame.geotech

Subaccessors
------------

.. autosummary::
   :template: autosummary/accessor.rst

   DataFrame.geotech.point

.. toctree::
   :hidden:

   point

.. _columns:

Columns
-------

:mod:`geotech-pandas` relies heavily in consistent column names and units. For now, SI units are
assumed throughout the package. The columns used throughout the package are summarized in the
following table:

.. list-table::
   :header-rows: 1

   * - Name
     - Unit
     - Description
   * - ``point_id``
     -
     - Point ID in which a layer belongs to.
   * - ``bottom``
     - m
     - Bottom depth of a layer.
   * - ``top``
     - m
     - Top depth of a layer.
   * - ``center``
     - m
     - Center depth of a layer.
   * - ``thickness``
     - m
     - Thickness of a layer.
