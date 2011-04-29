#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import logging
import urllib
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from collective.opensearch import opensearchMessageFactory as _
from collective.opensearch.browser import oslinkview


class IMapView(Interface):
    """
    Html view interface
    """

class MapView(oslinkview.OsLinkView):
    """
    Html browser view
    """
    implements(IMapView)

    def download_url(self):
        return self.context.absolute_url() + '/@@opensearch_link.kml?' + urllib.quote_plus(self.searchterm)



