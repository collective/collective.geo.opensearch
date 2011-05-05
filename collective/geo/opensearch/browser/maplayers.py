#
import urllib
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer

class FeedMapLayer(MapLayer):
    """
    a layer for a Feed
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request


    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        context_url += '@@opensearch_link.kml?searchTerms=' + urllib.quote_plus(
                self.request.form.get('searchTerms',''))
        return"""
        function() { return new OpenLayers.Layer.GML('%s', '%s',
            { format: OpenLayers.Format.KML,
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}
        """ % (self.context.Title().decode('utf-8', 'ignore'
                                ).encode('ascii', 'xmlcharrefreplace'
                                ).replace("'", "&apos;"), context_url)
class KMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(FeedMapLayer(self.context, self.request))
        return layers


class KMLFolderMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLFolderMapLayers, self).layers()
        type_filter = {"portal_type" : ["Link"]}
        for r in self.context.getFolderContents(contentFilter=type_filter):
            obj = r.getObject()
            if obj.getLayout() == 'feed_map_view.html':
                layers.append(FeedMapLayer(obj, self.request))
        return layers
