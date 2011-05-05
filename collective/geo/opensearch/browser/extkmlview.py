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
import cgi
import logging
import shapely.geometry as geom
from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from utils import parse_geo_rss
from collective.opensearch.browser.utils import fetch_url, substitute_parameters

logger = logging.getLogger('collective.geo.opensearch')

def coords_to_kml(geom):
    gtype = geom['type']
    coordlist = []
    mg_tmpl = '%s'
    if gtype == 'Point':
        coordlist.append( (geom['coordinates'],))
        tmpl = '''
            <Point>
              <coordinates>%s</coordinates>
            </Point>'''
    elif gtype == 'Polygon':
        coordlist = geom['coordinates']
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
        coordlist.append(geom['coordinates'])
        tmpl = '''
            <LineString>
              <coordinates>
                %s
              </coordinates>
            </LineString>'''
    elif gtype == 'MultiPolygon':
        coordlist = geom['coordinates']
        mg_tmpl = '''
            <MultiGeometry>
                %s
            </MultiGeometry>'''
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

    else:
        raise ValueError, "Invalid geometry type"
    templates = []
    for coords in coordlist:
        if len(coords[0]) == 2:
            tuples = ('%f,%f,0.0' % tuple(c) for c in coords)
        elif len(coords[0]) == 3:
            tuples = ('%f,%f,%f' % tuple(c) for c in coords)
        else:
            raise ValueError, "Invalid dimensions"
        templates.append(tmpl % ' '.join(tuples))
    return mg_tmpl % '\n'.join(templates)


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

    def has_searchterm(self):
        url = self.context.getRemoteUrl()
        return url.find('%7BsearchTerms%7D') > 0

    @property
    def searchterm(self):
        return self.request.form.get('searchTerms', '')

    def cdata_desc(self, entry):
        def html_desc(description, entry):
            desc = u'<p>' + cgi.escape(description) +u'</p>'
            links = entry.get('links',[])
            alt_links = []
            for link in links:
                alt_link = {}
                if link.get('rel') == 'alternate':
                    if link.get('title'):
                        alt_link['title'] = link['title']
                    elif link.get('type') !='text/html':
                        # text/html is the default assigned by
                        # feedparser so this is meaningless
                        alt_link['title'] = link['type']
                    elif link.get('href'):
                        alt_link['title'] = link['href']
                    else:
                        continue
                    if link.get('href'):
                        alt_link['href'] = link['href']
                    else:
                        continue
                alt_links.append(alt_link)
            if alt_links:
                desc +=u'<p><ul>'
                for link in alt_links:
                    desc += u'<li><a href="%(href)s">%(title)s</a></li>' % link
                desc +=u'</ul></p>'
            return desc

        sd = entry.get('summary_detail')
        if sd:
            if sd['type'] in ['text/html', 'application/xhtml+xml']:
                summary =sd['value']
            elif sd['type'] == 'text/plain':
                summary = html_desc(sd['value'], entry)
            else:
                logger.debug('unrecognised summary type: %s' % sd['type'])
                summary = cgi.escape(sd['value'], entry)
        elif entry.get['content']:
            content = entry['content'][0]
            if content['type'] in ['text/html', 'application/xhtml+xml']:
                summary = content['value']

            elif content['type'] == 'text/plain':
                summary = html_desc(content['value'], entry)
            else:
                logger.debug('unrecognised summary type: %s' % content['type'])
                summary = cgi.escape(content['value'])
        else:
            logger.info('no description found for entry')
            summary =  html_desc(u'No Description', entry)
        return  '<![CDATA[ %s ]]>' % summary


    def entries(self):
        for entry in self.results.entries:
            try:
                geo = parse_geo_rss(entry)
                if geo:
                    g = geom.asShape(geo)
                    entry['kml_coordinates'] = coords_to_kml(geo)
                    entry['get_description'] = self.cdata_desc(entry)
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
        if self.has_searchterm():
            if not search_term:
                    return []
        qurl = substitute_parameters(url, self.request.form)
        rd = fetch_url(qurl)
        self.results = rd['result']
        self.request.RESPONSE.setHeader('Content-Type',
            '%s; charset=utf-8' % self._type)
        if rd['type'] == 'feed':
            return self.render()
        elif rd['type'] == 'kml':
            return self.results
