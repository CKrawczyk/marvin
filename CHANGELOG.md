# Marvin's Change Log

## [2.1.5] - unreleased
### Added:
- Better BPT documentation, in particular in the `Modifying the plot` section.
- A hack function ``marvin.utils.plot.utils.bind_to_figure()`` that replicate the contents of a matplotlib axes in another figure.

### Changed:
- Issue #190: ``Maps.get_bpt()`` and ``marvin.utils.dap.bpt.bpt_kewley06()`` now also return a list of axes. Each axes contains a method pointing to the ``marvin.utils.plot.utils.bind_to_figure()`` function, for easily transfer the axes to a new figure.

### Fixed:


## [2.1.4] - 2017/08/02
### Added:
- Added new query_params object, for easier navigation of available query parameters.  Added new tests.
- Added a new guided query builder using Jquery Query Builder to the Search page
- Added a View Galaxies link on the web results to view postage stamps of the galaxies in the results
- Added Route Rate Limiting.  Adopts a limit of 200/min for all api routes and 60/minute for query api calls and web searches

### Changed:
- Changed call signature for :meth:`marvin.utils.plot.map.no_coverage_mask` (removed ``value`` arg because unused, added ``None`` as default value ``ivar`` (``None``), and re-ordered args and kwargs).
- Changed call signature for :meth:`marvin.utils.plot.map.bad_data_mask` (removed ``value`` arg because unused).
- Changed the Marvin web search page to use the new query_params and parameter grouping.  Removed the autocomplete input box.
- Updated the documentation on query and query_params.
- Modified Guided Search operator options to remove options that could not be parsed by SQLA boolean_search
- Refactored the web settings, route registration, extensions to enable extensibility
- Issue #282: Improvements to "Go to CAS" link.  Changed to Go To SkyServer and updated link to public up-to-date link

### Fixed:
- Issue #102: problem with urllib package when attempting to retrieve the Marvin URLMap
- Issue #93: safari browser does not play well with marvin
- Issue #155: Contrails in Web Map
- Issue #174: sdss_access may not be completely python 3 compatible
- Issue #196: Bin not loading from local sas
- Issue #207: Get Maps in MapSpecView of Galaxy page sometimes fails to return selected maps
- Issue #210: pip upgrade may not install new things as fresh install
- Issue #209: marvin version from pip install is incorrect
- Issue #268: Cube flux from file error
- Issue #85: Python does not start in Python 3
- Issue #273: ha.value bug
- Issue #277: Ticks for log normalized colorbar
- Issue #275: logger crashes on warning when other loggers try to log
- Issue #258: 422 Invalid Parameters
- Issue #271: Problem in dowloading image.
- Issue #97: sqlalchemy-boolean-search not found when installed from pip source
- Issue #227: Marvin installation in python 3.6 (update setuptools to 36)
- Issue #262: problem with marvin update
- Issue #270: BPT array sizing not compatible
- Issue #88: Deployment at Utah requires automatisation
- Issue #234: Add (and use) functions to the datamodel to determine plotting parameters
- Issue #278: marvin_test_if decorator breaks in python 2.7
- Issue #274: cube slicing to get a spaxel fails with maps error
- Issue #39: implement more complete testing framework
- Issue #242: Result object representation error with 0 query results
- Issue #159: Marvin issues multiple warnings in PY3
- Issue #149: Improve integrated flux maps display in web

## [2.1.3] - 2017/05/18
### Added:
- Issue #204: added elpetro_absmag colours to mangaSampleDB models.
- Issue #253: Plotting tutorial.
- Issue #223: Easy multi-panel map plotting (with correctly placed colorbars).
- Issue #232 and Issue #251: Uses matplotlib style sheets context managers for plotting (map, spectrum, and BPT) and restores previous defaults before methods finish.
- Issue #189: Map plotting accepts user-defined value, ivar, and/or mask (including BPT masks).
- Issue #252: Quantile clipping for properties other than velocity, sigma, or flux in web.
- Added `utils.plot.map` doc page.
- Added `tools.map` doc page.

### Changed:
- Issue #243: inverted `__getitem__` behaviour for Cube/Maps/ModelCube and fixed tests.
- Modified Flask Profiler File to always point to $MARVIN_DIR/flask_profiler.sql
- Issue #241: Moved map plotting methods from tools/map to utils/plot/map
- Issue #229 and Issue #231: Switch to new gray/hatching scheme (in tools and web):
  - gray: spaxels with NOCOV.
  - hatched: spaxels with bad data (UNRELIABLE and DONOTUSE) or S/N below some minimum value.
  - colored: good data.
- Issue #238: Move plot defaults to datamodel (i.e., bitmasks, colormaps, percentile clips, symmetric, minimum SNR).
- Issue #206: SNR minimum to None (effectively 0) for velocity maps so that they aren't hatched near the zero velocity contour.
- Simplified default colormap name to "linearlab."
- Decreased map plot title font size in web so that it does not run onto second line and overlap plot.

### Fixed:
- Interactive prompt for username in sdss_access now works for Python 3.
- Fixed #195: The data file for the default colormap for `Map.plot()` ("linear_Lab") is now included in pip version of Marvin and does not throw invalid `FileNotFoundError` if the data file is missing.
- Fixed #143: prevents access mode to go in to remote if filename is present.
- Fixed #213: shortcuts are now only applied on full words, to avoid blind replacements.
- Fixed #206: no longer masks spaxels close to zero velocity contour in web and tools map plots
- Fixed #229: corrects web bitmask parsing for map plots
- Fixed #231: hatch regions within IFU but without data in map plots
- Fixed #255: Lean tutorial code cells did not work with the ipython directive, so they now use the python directive.
- Highcharts draggable legend cdn.

### Removed:
- Issue #232 and Issue #251: Automatic setting of matplotlib style sheets via seaborn import or `plt.style.use()`.


## [2.1.2] - 2017/03/17
### Added:
- API and Web argument validation using webargs and marshmallow.  If parameters invalid, returns 422 status.

### Changed:
- Per Issue #186: Switched to using the elpetro version of stellar mass, absolute magnitude i-band, and i-band mass-to-light ratio for NSA web display, from sersic values. (elpetro_logmass, elpetro_absmag_i, elpetro_mtol_i)
- Issue #188: deprecated snr in favour of snr_min for get_bpt. snr can still be used.
- Issue #187: Renamed NSA Display tab in web to Galaxy Properties.  Added a link to the NASA-Sloan Atlas catalogue to the table title.
- Moved our documentation to readthedocs for version control.  Updated all Marvin web documenation links to point to readthedocs.

### Fixed:
- A bug in the calculation of the composite mask for BPT.
- Issue #179: Fixed a python 2/3 exception error compatibility with the 2.1 release.


## [2.1.1] - 2017/02/18
### Added:
- Added query runtime output in search page html. And a warning if query is larger than 20 seconds.

### Changed:
- Removed the python 3 raise Exception in the check_marvin bin
- Reverted the api/query return output from jsonify back to json.dumps
    - This is an issue with python 2.7.3 namedtuple vs 2.7.11+

### Fixed:
- Issue #181: web display of maps were inverted; changed to xyz[jj, ii, val] in heatmap.js
- Added more code to handle MarvinSentry exceptions to fix #179.


## [2.1.0] - 2017/02/16
### Added:
- Restructured documentation index page.
- Improved installation documentation:
    - Removed old installation text
    - Added section on marvin SDSS dependencies and SAS_BASE_DIR
    - Added section for FAQ about installation
    - Added web browser cache issue into FAQ
- Added traceback info in the API calls
    - Added traceback attribute in Brain config
    - Added hidden _traceback attribute in Marvin config
    - Only implemented in two Query API calls at the moment
    - Added a few tests for traceback
    - see usage in cube_query in marvin/api/query.py
- Added the Ha_to_Hb ratio the DAP ModelClasses for querying
- Added new script to perform somce basic system, os, and Marvin checks: bin/check_marvin
- Added an alert banner when the user is using Safari. See #94.
- Issue #122: added ra/dec to spaxel
- Issue #145: Limited the number of query parameters in the web
- Added more tests to Results for sorting, paging, and getting subsets
- Added kwargs input for Spaxel when using Result.convertToTool
- Added automatic Sentry error logging #147 into MarvinError, and Sentry in Flask for production mode
- Added custom error handlers for the web, with potential user feedback form
- Added Sentry tool for grabbing and displaying Sentry statistics
- Added text to MarvinError with a Github Issues link and description of how to submit and issue
- Added Results option to save to CSV
- Added new parameters in Marvin Config to turn off Sentry error handling and Github Issue message
- Added Python example code for getting a spectrum in galaxy page of web.
- Added new test for image utilities getRandomImages, getImagesByPlate, getImagesByList
- Added new documentation on Image Utilities
- Added new image utility function showImage, which displays images from your local SAS
- Added the Kewley+06 implementation of the BPT classification as `Maps.get_bpt()`
- Added quick access to the NSA information for a Cube/Maps either from mangaSampleDB or drpall.

### Changed:
- When marvin is running from source (not dist), `marvin.__version__` is `dev`.
- Removed the cleanUpQueries method to assess db stability
- Switched dogpile.cache from using a file to python-memcached
- Syntax changes and bug fixes to get Marvin Web working when Marvin run on 3.5
- Got Queries and Results working in 3.5
- Changed all convertToTool options in Results from mangaid to plateifu
- Added release explicitly into api query routes
- Modified the decision tree in query to throw an error in local mode
- Modified convertToTool to accept a mode keyword
- Modifed the MarvinError for optional Sentry exception catching, and github issue inclusion
- Updated all Marvin tests to turn off Sentry exception catching and the github message
- Updated some of the Tools Snippets on the web
- Overhauled Map plotting
    - uses DAP bitmasks (NOVALUE, BADVALUE, MATHERROR, BADFIT, and DONOTUSE)
    - adds percentile and sigma clipping
    - adds hatching for regions with data (i.e., a spectrum) but no measurement by the DAP
    - adds Linear Lab color map
    - adds option for logarithmic colorbar
    - adds option to use sky coordinates
    - adds map property name as title
    - makes plot square
    - sets plotting defaults:
        - cmap is linear_Lab (sequential)
        - cmap is RdBu_r (diverging) for velocity plots (Note: this is reversed from the sense of the default coolwarm    colormap in v2.0---red for positive velocities and blue for negative velocities)
        - cmap is inferno (sequential) for sigma plots
        - clips at 5th and 95th percentiles
        - clips at 10th and 90th percentiles for velocity and sigma plots
        - velocity plots are symmetric about 0
        - uses DAP bitmasks NOVALUE, BADVALUE, MATHERROR, BADFIT, and DONOTUSE
        - also masks spaxels with ivar=0
        - minimum SNR is 1
- Changed Marvin Plate path back to the standard MarvinToolsClass use
- Made sdss_access somewhat more Python 3 compatible
- Modified the image utilities to return local paths in local/remote modes and url paths when as_url is True
- downloadList utility function now downloads images
- updated the limit-as parameter in the uwsgi ini file to 4096 mb from 1024 mb for production environment

### Fixed:
- Issue #115: drpall does not get updated when a tool sets a custom release.
- Issue #107: missing os library under save function of Map class
- Issue #117: hybrid colours were incorrect as they were being derived from petroth50_el.
- Issue #119: test_get_spaxel_no_db fails
- Issue #121: bugfix with misspelled word in downloadList utility function
- Issue #105: query results convertToTool not robust when null/default parameters not present
- Issue #136: BinTest errors when nose2 run in py3.5 and marvin server in 3.5
- Issue #137: PIL should work in py2.7 and py3.5
- Issue #172: broken mode=auto in image utilities
- Issue #158: version discrepancy in setup.py

## [2.0.9] - 2016/11/19
### Added:
- Docs now use `marvin.__version__`.

### Fixed:
- Fixed #100, #103: problem with getMap for properties without ivar.
- Fixed #101: problem with marvin query.


## [2.0.8] - 2016/11/18
### Fixed:
- Now really fixing #98


## [2.0.7] - 2016/11/18
### Fixed:
- Fixed issue #98


## [2.0.6] - 2016/11/17
### Fixed:
- Bug in Queries with dap query check running in remote mode.  Param form is empty.


## [2.0.5] - 2016/11/17
### Added:
- Added netrc configuration to installation documentation.
- Added netrc check on init.

### Fixed:
- Added mask to model spaxel.
- Bug in Cube tool when a galaxy loaded from db does not have NSA info; no failure with redshift
- Two bugs in index.py on KeyErrors: Sentry issues 181369719,181012809
- Bug on plate web page preventing meta-data from rendering
- Fixed installation in Python 3.
- Fixed long_description in setup.py to work with PyPI.
- Fixed a problem that made marvin always use the modules in extern


## [The dark ages] - multiple versions not logged.


## [1.90.0]
### Changed
- Full refactoring of Marvin 1.0
- Refactored web

### Added
- Marvin Tools
- Queries (only global properties, for now)
- Point-and-click for marvin-web
- RESTful API
- Many more changes

### Fixed
- Issue albireox/marvin#2: Change how matplotlib gets imported
