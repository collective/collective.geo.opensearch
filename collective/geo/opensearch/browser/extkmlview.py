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

import urllib
import feedparser
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

import shapely.geometry as geom
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from utils import parse_geo_rss
#from collective.geo.kml.browser.kmldocument import coords_to_kml

def coords_to_kml(geom):
    gtype = geom['type']
    if gtype == 'Point':
        coords = (geom['coordinates'],)
        tmpl = '''
            <Point>
              <coordinates>%s</coordinates>
            </Point>'''
    elif gtype == 'Polygon':
        coords = geom['coordinates'][0]
        tmpl = '''
            <Polygon>
              <outerBoundaryIs>
                <LinearRing>
                  <coordinates>
                    %s
                  </coordinates>
                </LinearRing>
              </outerBoundaryIs>
            </Polygon>'''
    elif gtype == 'LineString':
        coords = geom['coordinates']
        tmpl = '''
            <LineString>
              <coordinates>
                %s
              </coordinates>
            </LineString>'''
    else:
        raise ValueError, "Invalid geometry type"

    if len(coords[0]) == 2:
        tuples = ('%f,%f,0.0' % tuple(c) for c in coords)
    elif len(coords[0]) == 3:
        tuples = ('%f,%f,%f' % tuple(c) for c in coords)
    else:
        raise ValueError, "Invalid dimensions"
    return tmpl % ' '.join(tuples)


class IExtKMLView(Interface):
    """
    Search Kml view interface
    """


class ExtKMLView(BrowserView):
    """
    FlexiTopicKml browser view
    """
    implements(IExtKMLView)
    render = ViewPageTemplateFile('extkmlview.pt')
    #_type="application/vnd.google-earth.kml+xml"
    _type="text/xml"
    results=[]

    @property
    def searchterm(self):
        return self.request.form.get('SearchableText', '')

    def entries(self):
        for entry in self.results.entries:
            try:
                geo = parse_geo_rss(entry)
                g = geom.asShape(geo)
                entry['kml_coordinates'] = coords_to_kml(geo)
                yield entry
            except ValueError:
                pass


    def get_link(self):
        return self.results.href

    def get_type(self):
        return self.results.headers['content-type']

    def __call__(self):
        url = self.context.getRemoteUrl()
        search_term = urllib.quote_plus(self.searchterm)
        if not search_term:
                return []
        qurl = url.replace('%7BsearchTerms%7D',search_term)
        self.results= feedparser.parse(qurl)

        self.request.RESPONSE.setHeader('Content-Type',
            '%s; charset=utf-8' % self._type)
        return self.render()
