from zope.interface import implements, Interface
from plone.memoize import view

from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark

from collective.opensearch.browser import search

class IKMLView(Interface):
    """
    Search Kml view interface
    """


class KMLView(KMLBaseDocument):
    """
    FlexiTopicKml browser view
    """
    implements(IKMLView)

    @property
    @view.memoize
    def features(self):
        search_results = search.get_results(self.context, self.request)
        for brain in search_results:
            if brain.zgeo_geometry:
                yield BrainPlacemark(brain, self.request, self)
