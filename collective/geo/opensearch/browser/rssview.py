from DateTime import DateTime
from zope.interface import implements, Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.opensearch.browser import rssview
from utils import get_geo_rss

class RSSEntry(rssview.RSSEntry):

    def geo_rss(self):
        return get_geo_rss(self, self.brain)

class IRSSView(Interface):
    """
    RSS view interface
    """


class RSSView(rssview.RSSView):
    """
    RSS browser view
    """
    implements(IRSSView)
    render = ViewPageTemplateFile('rssview.pt')
    LinkEntry = RSSEntry



