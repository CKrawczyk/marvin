
.. _marvin-query:

Query
=====

.. _marvin-query_getstart:

Getting Started
^^^^^^^^^^^^^^^

The basic usage of searching the MaNGA dataset with Marvin Queries is shown below.  Queries allow you to perform searches filtering the sample on specific parameter conditions, as well as return additional desired parameters.  Queries accept two basic keywords, **searchfilter** and **returnparams**.

You search the MaNGA dataset by constructing a string filter condition in a pseudo-SQL syntax of **parameter operand value**.  You only need to care about constructing your filter or **where clause**, and Marvin will do the rest.

* **Condition I Want**: find all galaxies with a redshift less than 0.1.
* **Constructor**: **Parameter**: 'redshift (z or nsa.z)' + **Operand**: less than (<) + **Value**: 0.1
* **Marvin Filter Syntax**: 'nsa.z < 0.1'

::

    from marvin.tools.query import Query

    # search for galaxies with an NSA redshift < 0.1
    myfilter = 'nsa.z < 0.1'

    # create a query
    query = Query(searchfilter=myfilter)

You can optionally return parameters using the **returnparams** keyword, specified as a list of strings.

::

    # return the galaxy RA and Dec as well
    myfilter = 'nsa.z < 0.1'
    myparams = ['cube.ra', 'cube.dec']

    query = Query(searchfilter=myfilter, returnparams=myparams)

To see what parameters are available for returning and searching on, see the :ref:`marvin_parameter_list` on the :ref:`marvin-query-parameters` page.

Finally, you can run the query with **run**.  Queries produce results.  Go to :ref:`marvin-results` to see how to manage your query results.

::

    results = query.run()

Queries will always return a set of default parameters: the galaxy **mangaid**, **plateifu**, **plate id**, and **ifu design name**.  Additionally, queries will always return any parameters used in your filter condition, plus any requested return parameters.

::

    # see the returned columns
    print(results.columns)
    [u'cube.mangaid', u'cube.plate', u'cube.plateifu', u'ifu.name', 'cube.ra', 'cube.dec', 'nsa.z']

    # look at the first row result
    print(results.results[0])
    (u'1-209232', 8485, u'8485-1901', u'1901', 232.544703894, 48.6902009334, 0.0407447)

.. _marvin_query_using

Using Query
^^^^^^^^^^^
.. toctree::
   :maxdepth: 2

   Using the Query <tools/query/query_using>

.. toctree::
   :maxdepth: 2

   Returning Marvin objects <tools/query/query_returntype>

.. toctree::
   :maxdepth: 2

   Saving Queries <tools/query/query_saving>

.. _marvin_query_api

Reference/API
^^^^^^^^^^^^^

.. rubric:: Class

.. autosummary:: marvin.tools.query.query.Query

.. rubric:: Methods

.. autosummary::

    marvin.tools.query.query.Query.run
    marvin.tools.query.query.Query.reset
    marvin.tools.query.query.Query.show
    marvin.tools.query.query.Query.save
    marvin.tools.query.query.Query.restore


|


