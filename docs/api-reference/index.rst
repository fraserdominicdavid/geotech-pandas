.. currentmodule:: pandas

=============
API Reference
=============
In geotech-pandas, various subaccessors provide scope-specific methods. These methods reside in
separate namespaces within :class:`~pandas.DataFrame.geotech`.

Most methods include a *Requires* block, which lists the columns required for that specific method.
Each listed column links to its corresponding entry in the :ref:`column-reference`.

.. admonition:: **Requires:**
   :class: important

   | :term:`point_id`
   | :term:`bottom`

If the required columns are missing from the DataFrame when calling a method, an error will be
raised. This error message will also list the missing columns. By default, :term:`point_id` and
:term:`bottom` are the minimum required columns. However, these two columns are generally not
defined in the *Requires* block unless the method explicitly uses them (e.g.,
:meth:`~pandas.DataFrame.geotech.layer.get_top`).

Accessor
--------

.. autosummary::
   :toctree: api/
   :template: autosummary/accessor.rst

   DataFrame.geotech
