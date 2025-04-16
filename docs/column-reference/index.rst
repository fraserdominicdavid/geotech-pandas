.. _column-reference:

================
Column Reference
================
geotech-pandas relies heavily on consistent column names and units. The package currently assumes
all units are in SI (International System of Units). These columns are summarized in the following
lists.

The columns are listed in the following format:

    column_name
        | Description
        | *unit*
        | ``dtype``

.. _general-columns:

General Columns
---------------
.. glossary::

    point_id
        | Point ID in which a layer belongs to.
        | *unitless*
        | ``string``

    bottom
        | Bottom depth of a layer.
        | *meters (m)*
        | ``float``

    top
        | Top depth of a layer.
        | *meters (m)*
        | ``float``
   
    center
        | Center depth of a layer.
        | *meters (m)*
        | ``float``
   
    thickness
        | Thickness of a layer.
        | *meters (m)*
        | ``float``

    sample_type
        | Type of sample.
        | *unitless*
        | ``string``

    sample_number
        | Sample ID number.
        | *unitless*
        | ``int``

.. _spt-columns:

SPT Columns
-----------
.. glossary::

    blows_1
        | Blow counts in the 1st SPT increment.
        | *blows per 150 millimeters (blows/150mm)*
        | ``int``

    blows_2
        | Blow counts in the 2nd SPT increment.
        | *blows per 150 millimeters (blows/150mm)*
        | ``int``

    blows_3
        | Blow counts in the 3rd SPT increment.
        | *blows per 150 millimeters (blows/150mm)*
        | ``int``
        
    pen_1
        | Length driven/penetrated by the sampler in the 1st SPT increment.
        | *millimeters (mm)*
        | ``float``

    pen_2
        | Length driven/penetrated by the sampler in the 2nd SPT increment.
        | *millimeters (mm)*
        | ``float``

    pen_3
        | Length driven/penetrated by the sampler in the 3rd SPT increment.
        | *millimeters (mm)*
        | ``float``

    seating_pen
        | SPT seating penetration, the penetration in the 1st increment.
        | *millimeters (mm)*
        | ``float``

    main_pen
        | SPT main penetration, the sum of the penetration in the 2nd and 3rd increments.
        | *millimeters (mm)*
        | ``float``

    total_pen
        | SPT total penetration, the sum of the penetration in all the increments.
        | *millimeters (mm)*
        | ``float``

    seating_drive
        | SPT seating drive, the number of blows required to drive the 1st increment.
        | *blows per 150 millimeters (blows/150mm)*
        | ``int``

    main_drive
        | SPT main drive, the sum of the number of blows required to drive the 2nd and 3rd
          increments.
        | *blows per 300 millimeters (blows/300mm)*
        | ``int``

    total_drive
        | SPT total drive, the sum of the number of blows required to drive all increments.
        | *blows per 450 millimeters (blows/450mm)*
        | ``int``

    is_refusal
        | Whether or not SPT samples are considered refusals.
        | *unitless*
        | ``bool``

    is_hammer_weight
        | Whether or not SPT samples are considered hammer weights.
        | *unitless*
        | ``bool``

    n_value
        | SPT N-value, equivalent to the main drive if a sample is not a refusal.
        | *blows per 300 millimeters (blows/300mm)*
        | ``int``

    spt_report
        | Simple descriptive SPT report.
        | *unitless*
        | ``string``

.. _soil-index-columns:

Soil Index Columns
------------------
.. glossary::

    {prefix}_mass_moist
        | Mass of container and moist specimen.
        | *grams (g)*
        | ``float``

    {prefix}_mass_dry
        | Mass of container and oven dry specimen.
        | *grams (g)*
        | ``float``

    {prefix}_mass_container
        | Mass of container.
        | *grams (g)*
        | ``float``

    {prefix}_moisture_content
        | Moisture content. The ratio of the mass of water contained in the pore spaces of soil or
          rock material, to the solid mass of particles in that material. A standard temperature of
          110 ± 5°C is used to determine these masses.
        | *percent (%)*
        | ``float``

        .. note::

            The `{prefix}` indicated here is used to specify the prefix when calculating the
            moisture content. By default, the prefix is "moisture_content", however if the prefix is
            "moisture_content", :term:`{prefix}_moisture_content` would then become just
            `moisture_content` alone to avoid confusion.

            Moisture content mass measurements do not necessarily require using *grams (g)*
            as the unit. However, maintaining **consistency** in the chosen units is essential.

    liquid_limit_{n}_drops
        | Number of drops causing closure of the groove for trial `{n}`.
        | *drops*
        | ``int``

    liquid_limit_{n}_moisture_content
        | Moisture content for trial `{n}`.
        | *percent (%)*
        | ``float``

        .. note::

            The `{n}` indicated here is used to specify the trial number when calculating the
            liquid limit.
    
    liquid_limit
        | Liquid limit. The water content of a soil at the arbitrarily defined boundary between the
          semi-liquid and plastic states.
        | *percent (%)*
        | ``float``

    plastic_limit_1_moisture_content
        | Moisture content for the first plastic limit test.
        | *percent (%)*
        | ``float``

    plastic_limit_2_moisture_content
        | Moisture content for the second plastic limit test.
        | *percent (%)*
        | ``float``

    plastic_limit
        | Plastic limit. The water content of a soil at the boundary between the plastic
          and semi-solid states.
        | *percent (%)*
        | ``float``

    is_nonplastic
        | Whether or not a layer is considered nonplastic.
        | *unitless*
        | ``bool``

    plasticity_index
        | Plasticity index. The range of water content over which a soil behaves plastically.
        | *percent (%)*
        | ``float``

    liquidity_index
        | Liquidity index. The ratio of the water content of a soil at a given condition/state minus
          its plastic limit, to its plasticity index.
        | *unitless*
        | ``float``
