#
import logging
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import shapely.geometry as geom

logger = logging.getLogger('collective.geo.opensearch')

# Point coordinates are a 2-tuple (lon, lat)
def _parse_georss_point(value):
    try:
        lat, lon = value.replace(',', ' ').split()
        return {'type': 'Point', 'coordinates': (float(lon), float(lat))}
    except Exception, e:
       logger.info('exeption raised in _parse_georss_point: %s' % e)

# Line coordinates are a tuple of 2-tuples ((lon0, lat0), ... (lonN, latN))
def _parse_georss_line(value):
    try:
        latlons = value.replace(',', ' ').split()
        coords = []
        for i in range(0, len(latlons), 2):
            lat = float(latlons[i])
            lon = float(latlons[i+1])
            coords.append((lon, lat))
        return {'type': 'LineString', 'coordinates': tuple(coords)}
    except Exception, e:
        logger.info('exeption raised in _parse_georss_line: %s' % e)

# Polygon coordinates are a tuple of closed LineString tuples.
def _parse_georss_polygon(value):
    try:
        latlons = value.replace(',', ' ').split()
        coords = []
        for i in range(0, len(latlons), 2):
            lat = float(latlons[i])
            lon = float(latlons[i+1])
            coords.append((lon, lat))
        return {'type': 'Polygon', 'coordinates': (tuple(coords),)}
    except Exception, e:
        logger.info('exeption raised in _parse_georss_polygon: %s' % e)

def parse_geo_rss(entry):
    """ This parses the georss of a feedparser entry
    @return None if no georss was found or
            GeoJSON-like Python geo interface
    """
    if 'georss_where' in entry:
        if 'gml_envelope' in entry:
            #XXX return smthng like a polygon
            pass
        elif ('gml_point' in entry) and ('gml_pos' in entry):
            # Point
            return _parse_georss_point(entry['gml_pos'])
        elif (('gml_polygon' in entry) and ('gml_exterior' in entry)
                and ('gml_linearring' in entry) and ('gml_polslist' in entry)):
            # Polygon
            return _parse_georss_polygon(entry['gml_polslist'])
        elif ('gml_linestring' in entry) and ('gml_polslist' in entry):
            # LineString
            return _parse_georss_line(entry['gml_polslist'])
    # some versions of feedparser do not put the namespace in front :(
    elif 'where' in entry:
        if 'envelope' in entry:
            #XXX return smthng like a polygon
            pass
        elif ('point' in entry) and ('pos' in entry):
            # Point
            return _parse_georss_point(entry['pos'])
        elif (('polygon' in entry) and ('exterior' in entry)
                and ('linearring' in entry) and ('polslist' in entry)):
            # Polygon
            return _parse_georss_polygon(entry['polslist'])
        elif ('linestring' in entry) and ('polslist' in entry):
            # LineString
            return _parse_georss_line(entry['polslist'])


def get_geo_rss(context, brain):
    if brain.zgeo_geometry:
        if brain.zgeo_geometry['type'] == None:
            return
        elif brain.zgeo_geometry['type'] == 'Point':
            coords = (brain.zgeo_geometry['coordinates'],)
            template = ViewPageTemplateFile('point.pt')

        elif brain.zgeo_geometry['type'] == 'Polygon':
            coords = brain.zgeo_geometry['coordinates'][0]
            template = ViewPageTemplateFile('polygon.pt')

        elif brain.zgeo_geometry['type'] == 'LineString':
            coords = brain.zgeo_geometry['coordinates']
            template = ViewPageTemplateFile('linestring.pt')

        # A bounding box defines a rectangular region.
        # It is often used to define the extents of a map or define a
        # rough area of interest. A GML box is called an Envelope.
        elif brain.zgeo_geometry['type'] == 'MultiPoint':
            geometry = geom.MultiPoint(brain.zgeo_geometry['coordinates']).bounds
            coords = [geometry,]
            template = ViewPageTemplateFile('envelope.pt')
        elif brain.zgeo_geometry['type'] == 'MultiLineString':
            geometry = geom.MultiLineString(brain.zgeo_geometry['coordinates']).bounds
            coords = [geometry,]
            template = ViewPageTemplateFile('envelope.pt')
        elif brain.zgeo_geometry['type'] == 'MultiPolygon':
            geometry = geom.MultiPolygon(brain.zgeo_geometry['coordinates']).bounds
            coords = [geometry,]
            template = ViewPageTemplateFile('envelope.pt')
        else:
            raise ValueError, "Invalid geometry type"
        if len(coords[0]) == 2 or len(coords[0]) == 3:
            tuples = ('%f %f' % (c[1], c[0]) for c in coords)
            return '\n'.join(template(
                            context, coords=' '.join(tuples)
                        ).split('\n')[1:])
        elif len(coords[0]) == 4 and len(coords) == 1:
            upper_corner=coords[0][2:4]
            lower_corner=coords[0][0:2]
            return '\n'.join(template(
                            context,
                            upper='%f %f' % upper_corner,
                            lower='%f %f' % lower_corner
                        ).split('\n')[1:])
        else:
            raise ValueError, "Invalid dimensions"

