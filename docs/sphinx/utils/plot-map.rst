.. _marvin-utils-plot-map:

==================================
Map (:mod:`marvin.utils.plot.map`)
==================================

.. _marvin-utils-plot-map-intro:

Introduction
------------
:mod:`marvin.utils.plot.map` contains utility functions for plotting Marvin maps.  The main function in this module is :func:`~marvin.utils.plot.map.plot`, which is thinly wrapped by the :meth:`~marvin.tools.map.Map.plot` method in the :class:`~marvin.tools.map.Map` class for convenience.


.. _marvin-utils-plot-map-getting-started:

Getting Started
---------------

:mod:`~marvin.utils.plot.map` makes plotting a publication-quality MaNGA map easy with its carefully chosen default parameters.

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    fig, ax = mapplot.plot(dapmap=ha)  # == ha.plot()

.. image:: ../_static/quick_map_plot.png


However, you may want to do further processing of the map, so you can override the default DAP :attr:`~marvin.utils.plot.map.plot.value`, :attr:`~marvin.utils.plot.map.plot.ivar`, and/or :attr:`~marvin.utils.plot.map.plot.mask` with your own arrays.

.. code-block:: python

    fig, ax = mapplot.plot(dapmap=ha, value=ha.value * 10.)


A :attr:`~marvin.utils.plot.map.plot.dapmap` object is not even necessary for :mod:`~marvin.utils.plot.map`, though if you do not provide a :attr:`~marvin.utils.plot.map.plot.dapmap` object, then you will need to set a :attr:`~marvin.utils.plot.map.plot.value`. You will also need to provide other attributes, such as :attr:`~marvin.utils.plot.map.plot.title` and :attr:`~marvin.utils.plot.map.plot.cblabel`, that are by default set from attributes of the :attr:`~marvin.utils.plot.map.plot.dapmap` object.

.. code-block:: python

    import numpy as np
    fig, ax = mapplot.plot(value=np.random.random((34, 34)), mask=ha.mask)


This flexibilty is especially useful for passing in a custom mask, such as one created with the :meth:`~marvin.tools.maps.Maps.get_bpt` method. For more explanation of the mask manipulation in this specific example, see the :ref:`plotting tutorial <marvin-plotting-map-starforming>`.

.. code-block:: python

    from marvin.tools.maps import Maps
    masks, __ = maps.get_bpt(show_plot=False)
    
    # Create a bitmask for non-star-forming spaxels by taking the
    # complement (`~`) of the BPT global star-forming mask (where True == star-forming)
    # and set bit 30 (DONOTUSE) for those spaxels.
    mask_non_sf = ~masks['sf']['global'] * 2**30
    
    # Do a bitwise OR between DAP mask and non-star-forming mask.
    mask = ha.mask | mask_non_sf
    fig, ax = mapplot.plot(dapmap=ha, mask=mask)  # == ha.plot(mask=mask)

.. image:: ../_static/map_bpt_mask.png


:mod:`~marvin.utils.plot.map` lets you build multi-panel plots because it accepts pre-defined `matplotlib.figure <http://matplotlib.org/api/figure_api.html>`_ and `matplotlib.axes <http://matplotlib.org/api/axes_api.html>`_ objects.

.. code-block:: python

    import matplotlib.pyplot as plt
    plt.style.use('seaborn-darkgrid')  # set matplotlib style sheet

    plateifus = ['8485-1901', '8485-1902', '8485-12701']
    mapnames = ['stellar_vel', 'stellar_sigma']

    rows = len(plateifus)
    cols = len(mapnames)
    fig, axes = plt.subplots(rows, cols, figsize=(8, 12))
    for row, plateifu in zip(axes, plateifus):
        maps = Maps(plateifu=plateifu)
        for ax, mapname in zip(row, mapnames):
            mapplot.plot(dapmap=maps[mapname], fig=fig, ax=ax, title=' '.join((plateifu, mapname)))

    fig.tight_layout()

.. image:: ../_static/multipanel_kinematics.png



.. _marvin-utils-plot-map-using:

Using :mod:`~marvin.utils.plot.map`
-----------------------------------

For more in-depth discussion of using :mod:`~marvin.utils.plot.map`, please see the following sections:

Plotting Tutorial
`````````````````

* :doc:`../tutorials/plotting`
  
  * :ref:`marvin-plotting-quick-map`
  * :ref:`marvin-plotting-multipanel-single`
  * :ref:`marvin-plotting-multipanel-multiple`
  * :ref:`marvin-plotting-custom-map-axes`
  * :ref:`Plot Halpha Map of Star-forming Spaxels <marvin-plotting-map-starforming>`
  * :ref:`Plot [NII]/Halpha Flux Ratio Map of Star-forming Spaxels <marvin-plotting-niiha-map-starforming>`


.. _marvin-utils-plot-map-default-params:

Default Plotting Parameters
```````````````````````````

====================  ====================  =========  ===============  ==================  ===========
MPL-5
-------------------------------------------------------------------------------------------------------
Property Type         Bad Data Bitmasks     Colormap   Percentile Clip  Symmetric Colorbar  Minimum SNR
====================  ====================  =========  ===============  ==================  ===========
default               UNRELIABLE, DONOTUSE  linearlab  5, 95            False               1
velocities            UNRELIABLE, DONOTUSE  RdBu_r     10, 90           True                0\ :sup:`a`
velocity dispersions  UNRELIABLE, DONOTUSE  inferno    10, 90           False               1
====================  ====================  =========  ===============  ==================  ===========

:sup:`a` Velocities do not have a minimum SNR. This allows spaxels near the zero-velocity contour to be displayed, but users are cautioned that some spaxels could have arbitrarily low SNRs.

**Note**: MPL-4 uses the same default plotting parameters as MPL-5, except the Bad Data Bitmasks, which use bit 1 (rough DONOTUSE) for all properties.


Masking
```````

Spaxels Not Covered by the IFU
::::::::::::::::::::::::::::::

:meth:`~marvin.utils.plot.map.no_coverage_mask` creates a mask of a map where there is no coverage by the IFU.

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    nocov = mapplot.no_coverage_mask(mask=ha.mask, bit=0, ivar=ha.ivar)


**Important**: In 2.1.3, the call signature is ``no_coverage_mask(value, ivar, mask, bit)``. In version 2.1.4, this changes to ``no_coverage_mask(mask, bit, ivar=None)``.


Spaxels Flagged as Bad Data
:::::::::::::::::::::::::::

:meth:`~marvin.utils.plot.map.bad_data_mask` creates a mask of a map where the data has been flagged by the DAP as UNRELIABLE or DONOTUSE.

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    bad_data = mapplot.bad_data_mask(mask=ha.mask, bits={'doNotUse': 30, 'unreliable': 5})


**Important**: In 2.1.3, the call signature is ``bad_data_mask(mask, bits)``. In version 2.1.4, this changes to ``bad_data_mask(mask, bits)``.


Spaxels with Low Signal-to-Noise
::::::::::::::::::::::::::::::::

:meth:`~marvin.utils.plot.map.low_snr_mask` creates a mask of a map where the data is below a minimum signal-to-noise ratio.

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    low_snr = mapplot.low_snr_mask(value=ha.value, ivar=ha.ivar, snr_min=1)


Spaxels with Negative Values
::::::::::::::::::::::::::::

:meth:`~marvin.utils.plot.map.log_colorbar_mask` creates a mask of a map where the values are negative.  This is necessary to avoid erros when using a logarithmic colorbar.

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    log_cb_mask = mapplot.log_colorbar_mask(value=ha.value, log_cb=True)


Combine Various Undesirable Masks
:::::::::::::::::::::::::::::::::

:meth:`~marvin.utils.plot.map.select_good_spaxels` creates a `NumPy masked array <https://docs.scipy.org/doc/numpy/reference/maskedarray.html>`_ that combines masks of undesirable spaxels (no IFU coverage, bad data, low signal-to-noise ratio, and negative values [if using a logarithmic colorbar]).

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    good_spax = mapplot.select_good_spaxels(value=ha.value, nocov=nocov, bad_data=bad_data, low_snr=low_snr, log_cb_mask=log_cb_mask)


Set the Plotting Extent for `imshow <https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.imshow.html>`_
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:meth:`~marvin.utils.plot.map.set_extent` returns the coordinates of the lower-left and upper-right corners of the map in cube coordinates (lower-left = (0, 0) and in units of spaxels) or sky coordinates (center = (0, 0) and in units of arcsec).

.. code-block:: python

    from marvin.tools.maps import Maps
    import marvin.utils.plot.map as mapplot
    maps = Maps(plateifu='8485-1901')
    ha = maps['emline_gflux_ha_6564']
    extent = mapplot.set_extent(cube_size=ha.value.shape, sky_coords=False)


Set Hatch Style
:::::::::::::::

:meth:`~marvin.utils.plot.map.set_patch_style` sets the style for the hatched region(s) that correspond to spaxels that are covered by the IFU but do not have usable data. :meth:`~marvin.utils.plot.map.plot` creates a single large hatched rectangle patch as the lowest layer and then places the gray background (no IFU coverage) and colored spaxels (good data) as higher layers.

.. code-block:: python

    import marvin.utils.plot.map as mapplot
    patch_kws = mapplot.set_patch_style(extent=extent, facecolor='#A8A8A8')


Axis Setup
::::::::::

:meth:`~marvin.utils.plot.map.ax_setup` sets the x- and y-labels and facecolor.


Set Title
:::::::::

:meth:`~marvin.utils.plot.map.set_title` sets the title of the axis object. You can directly specify the title or construct it from the property name (and channel name).

.. code-block:: python

    import marvin.utils.plot.map as mapplot
    title = mapplot.set_title(title=None, property_name=ha.property_name, channel=ha.channel)

Reference/API
-------------

.. rubric:: Module

.. autosummary:: marvin.utils.plot.map

.. rubric:: Functions

.. autosummary::

    marvin.utils.plot.map.ax_setup
    marvin.utils.plot.map.bad_data_mask
    marvin.utils.plot.map.log_colorbar_mask
    marvin.utils.plot.map.low_snr_mask
    marvin.utils.plot.map.no_coverage_mask
    marvin.utils.plot.map.plot
    marvin.utils.plot.map.select_good_spaxels
    marvin.utils.plot.map.set_extent
    marvin.utils.plot.map.set_patch_style
    marvin.utils.plot.map.set_title
