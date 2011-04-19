from zope.interface import implements, Interface
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.opensearch.browser import atomview
from utils import get_geo_rss

class AtomEntry(atomview.AtomEntry):

    def geo_rss(self):
        return get_geo_rss(self, self.brain)



class IAtomView(Interface):
    """
    Atom view interface
    """



class AtomView(atomview.AtomView):
    """
    Atom browser view
    """
    implements(IAtomView)
    render = ViewPageTemplateFile('atomview.pt')
    LinkEntry = AtomEntry



