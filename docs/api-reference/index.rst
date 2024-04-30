.. currentmodule:: pandas

=============
API Reference
=============
In geotech-pandas, scope-specific methods under various subaccessors are provided. These are
separate namespaces within :class:`~pandas.DataFrame.geotech`.

Accessor
--------

.. autosummary::
   :toctree: api/
   :template: autosummary/accessor.rst

   DataFrame.geotech

.. _columns:

Columns
-------
There is a heavy reliance in consistent column names and units in geotech-pandas. For now, SI units
are assumed throughout the package. The columns used throughout the package are summarized in the
following table:

Common Columns
^^^^^^^^^^^^^^
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
   * - ``sample_type``
     -
     - Type of sample.
   * - ``sample_number``
     -
     - Sample ID number.

.. _columns_spt:

SPT Columns
^^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Unit
     - Description
   * - ``blows_n``
     - blows/150mm
     - Blow counts in the nth SPT increment.
   * - ``pen_n``
     - mm
     - Length driven/penetrated by the sampler in the nth SPT increment.
   * - ``seating_pen``
     - mm
     - SPT seating penetration, the penetration in the 1st increment.
   * - ``main_pen``
     - mm
     - SPT main penetration, the sum of the penetration in the 2nd and 3rd increments.
   * - ``total_pen``
     - m
     - SPT total penetration, the sum of the penetration in all the increments.
   * - ``seating_drive``
     - blows
     - SPT seating drive, the number of blows required to drive the 1st increment.
   * - ``main_drive``
     - blows
     - SPT main drive, the sum of the number of blows required to drive the 2nd and 3rd increments.
   * - ``total_drive``
     - blows
     - SPT main drive, the sum of the number of blows required to drive all increments.
   * - ``is_refusal``
     -
     - Whether or not SPT samples are considered refusals.
   * - ``is_hammer_weight``
     -
     - Whether or not SPT samples are considered hammer weights.
   * - ``n_value``
     - blows/300mm
     - SPT N-value, equivalent to the main drive if a sample is not a refusal.
   * - ``spt_report``
     -
     - Simple descriptive SPT report.

.. _columns_lab_index:

Soil Index Columns
^^^^^^^^^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Name
     - Unit
     - Description
   * - ``moisture_content_mass_moist``
     - g
     - Mass of container and moist specimen.
   * - ``moisture_content_mass_dry``
     - g
     - Mass of container and oven dry specimen.
   * - ``moisture_content_mass_container``
     - g
     - Mass of container.
   * - ``moisture_content``
     - %
     - Moisture content.
