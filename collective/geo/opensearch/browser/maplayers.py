#
import urllib
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer

class FeedMapLayer(MapLayer):
    """
    a layer for a KML File.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request


    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'
        context_url += '@@opensearch_kml.kml?SearchableText=' + urllib.quote_plus(
                self.request.form.get('SearchableText',''))
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
                                ).replace("'", ""), context_url)
class KMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(FeedMapLayer(self.context, self.request))
        return layers
