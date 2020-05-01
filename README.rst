Introduction
============


``collective.geo.opensearch`` builds on `collective.geo`_ (Plone Maps) and `collective.opensearch`_.

Produce Spatial Open Search Feeds
----------------------------------

``collective.geo.opensearch`` adds the possibility to add OpenSearch
compatible search results to your Plone site.

* site wide: this is a simple copy of the Plone search so all option
  that you may pass to the standard /search will be recognized as well.

* for a collection/topic: You can search inside a topic, i.e. you
  define a 'base query' as a topic and additional parameters of the query
  are applied additional.


OpenSearch is a collection of simple formats for the sharing of search results.

OpenSearch helps search engines and search clients communicate by
introducing a common set of formats to perform search requests and
syndicate search results. OpenSearch helps search engines and search
clients communicate by introducing a common set of formats to perform
search requests and syndicate search results. The OpenSearch description
document format can be used to describe a search engine so that it can
be used by search client applications. The OpenSearch response elements
can be used to extend existing syndication formats, such as RSS and
Atom, with the extra metadata needed to return search results

collective.geo.opensearch enables you to syndicate the search results
of your Plone site by formatting them in the RSS, Atom or KML formats,
augmented with OpenSearch response elements.

Implemented extensions and conventions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- opensearch
- relevance
- opensearch description for autodiscovery
- suggestions so that browsers can autocomplete
- response elements and first, previous, next, last links
- georss (for Atom and RSS Results)


Consume Open Search Feeds
-------------------------

``collective.geo.opensearch`` adds a view to the link type that lets you
search OpenSearch (or other searches that return RSS or Atom, pretty
much any other format feed parser supports and KML) compatible search
providers within your site. The feeds do not need to implement
the opensearch extensions it suffices that they are valid feeds. As
there is no way of knowing if the feed returns georss or KML you have to
choose 'Open Search Map View' manually for this link.

You can combine several open search links as a metasearch. All OpenSearch
links inside a folder will be queried and their results displayed when
you change the view of a folder to 'Open Search Map View'

Usage:
------

1) Display a map view of a georss RSS, Atom or KML search results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a link content type that points to a remote (search) feed or KML.
You have to choose 'Open Search Map View' manually for this link.

georss feeds will be converted into a html search result and a KML
map layer. KML sources will be passed on 'as is' (the description
is passed through htmllaundry) and the name and description of the placemarks
displayed as search results.

The view consists of a simple search form, the map displaying the georss
or KML information and the results of the query

2) search multiple sources at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build a simple metasearch create a folder and add your query links to it.
Change the view of the folder to 'Open Search Map View'.
The view consist of a search form (currently only for full text search)
which input will be applied to all open search links (i.e. any link
that has 'Open Search Map View' set as its view). The results of
the searches will be displayed as layers in the map and in tabs beneath
the form. The queries are executed asynchronously via AJAX, so you do
not have to wait until the last query has finished.

Abusing collective.geo.opensearch to Display miscellaneous Feeds and KMLs
-------------------------------------------------------------------------

3) Display an arbitrary 'static' feed or a remote KML Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although the main focus of this product is to produce and display
search feeds you may use it to display any valid feed. If the url of the
link you added does not contain the {searchTerm} parameter and 'Open Search Map View'
(you have to select the view manually from the 'display' menu) is
selected as the view of the link, the feed will be fetched regardless of
the presence of a query parameter and its results will be displayed.
The search form will not be displayed in the absence of the
{searchTerms} parameter.

4) Display multiple feeds or KMLs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add your feeds to display to a folder (as in [2]) and select'Open Search Map View'
as the display view of the folder All feeds that do not have a
{searchTerm} parameter in their url will be fetched immediately,
regardless if a search input was provided. The search form will only be
displayed if at least one of the links inside the folder has a
{searchTerm} parameter.

5) Use collective.geo.opensearch to search inside your collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As opensearch results are added to all collections you may use it as a
search form to search inside your collections. if you use a relative
link (e.g. /mycollection/SearchableText={searchTerms}) you have to
choose 'Open Search Map View' manually to display the search results.

Known limitations issues and caveats
------------------------------------

- Currently only the {searchTerms} parameter for full text search is recognized and supported
- add '<match path="regex:^.*/opensearchresults.html*" abort="1" />' to your deliverance/xdv/diazo rules
- internal searches as described in [5] will always be executed as 'anonymous'
- relative links in kml files will not be rewritten

Differences between RSS/Atom and KML Search Results
---------------------------------------------------

The KML file will only return the content which is geo annotated.
RSS and Atom feeds will return all content that matches the query with
georss for the items which are geo annotated.


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


Translations
============

This product has been translated into

- Spanish.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Installation
============

This addon can be installed has any other addons, please follow official
documentation_.


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.geo.opensearch/master.svg
    :target: https://travis-ci.org/collective/collective.geo.opensearch

.. image:: http://img.shields.io/pypi/v/collective.geo.opensearch.svg
   :target: https://pypi.org/project/collective.geo.opensearch


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.opensearch/issues
- Source Code: https://github.com/collective/collective.geo.opensearch
- Documentation: https://collectivegeo.readthedocs.io/


License
=======

The project is licensed under the GPLv2.

.. _collective.geo: https://pypi.org/project/collective.geo.bundle
.. _collective.opensearch: https://pypi.org/project/collective.opensearch
.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: https://docs.plone.org/manage/installing/installing_addons.html
