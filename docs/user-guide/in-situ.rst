===================
In-Situ Subaccessor
===================
In geotech-pandas, the :class:`~pandas.DataFrame.geotech.in_situ` subaccessor is simply a namespace
that contains other subaccessors with methods that deal with in-situ tests. In general, the methods
in these subaccessors only handle raw in-situ test data. For example, a method that reads the blow
counts of each increment in a standard penetration test and returns the equivalent N-value. These
subaccessors are further discussed in the following sections.

.. toctree::
    :maxdepth: 1

    in-situ.spt
