Introduction
============


Collective.geo.Opensearch builds on collective.geo (Plone Maps) and collective.opensearch.

Produce Spatial Open Search Feeds
----------------------------------

collective.geo.opensearch adds the possibility to add OpenSearch compatible search results to your Plone site.

site wide: this is a simple copy of the plone search so all option
 that you may pass to the standard /search will be recognized as well.
for a collection/topic: You can search inside a topic, i.e. you
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
 of your plone site by formatting them in the RSS, Atom or KML formats,
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

collective.geo.opensearch adds a view to the link type that lets you
 search OpenSearch (or other searches that return RSS or Atom, pretty
 much any other format feed parser supports and KML) compatible search
 providers within your site. The feeds do not need to implement
 the opensearch extensions it suffices that they are valid feeds. As
 there is no way of knowing if the feed returns georss or KML you have to
 choose 'Open Search Map View' manually for this link.

You can combine several open search links as a metasearch. All OpenSearch links inside a folder will be queried and their results displayed when you change the view of a folder to 'Open Search Map View'

Usage:
------

1) Display a map view of a georss RSS, Atom or KML search results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a link content type that points to a remote (search) feed or KML. You have to choose 'Open Search Map View' manually for this link.

georss feeds will be converted into a html search result and a kml
 map layer. kml sources will be passed on 'as is' (so be cautious
of malicious html) and the name and description of the placemarks displayed as search results.

The view consits of a simple searchform, the map displaying the georss or kml information and the results of the query

2) search multiple sources at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To build a simple metasearch create a folder and add your query links to it. Change the view of the folder to 'Open Search Map View'.
 The view consist of a search form (currently only for full text search)
 which input will be applied to all open search links (i.e. any link
 that has 'Open Search Map View' set as its view). The results of
 the searches will be displayed as layers in the map and in tabs beneath
 the form. The queries are executed asynchronously via AJAX, so you do
 not have to wait until the last query has finished.

Abusing collective.geo.opensearch to Display miscelaneous Feeds and KMLs
------------------------------------------------------------------------

3) Display an abritary 'static' feed or a remote KML Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Allthough the main focus of this product is to produce and display
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
 searchform to search inside your collections. if you use a relative
 link (e.g. /mycollection/SearchableText={searchTerms}) you have to
 choose 'Open Search Map View' manually to display the search results.

Known limitations issues and caveats
------------------------------------

- Currently only the {searchTerms} paramter for full text search is recognized and supported
- add '<match path="regex:^.*/opensearchresults.html*" abort="1" />' to your deliverance/xdv/diazo rules
- internal searches as described in [5] will always be executed as 'anonymous'
- No html sanitation for kml description
- relative links in kml files will not be rewritten

Differences between RSS/Atom and KML Search Results
---------------------------------------------------

The KML file will only return the content which is geo annotated. RSS and Atom feeds will return all content that matches the query with georss for the items which are geo annotated.


- Code repository: http://svn.plone.org/svn/collective/collective.geo.opensearch/
- Report bugs at http://plone.org/products/collective.geo.opensearch/issues
