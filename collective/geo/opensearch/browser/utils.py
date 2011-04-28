#
import logging
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import shapely.geometry as geom

logger = logging.getLogger('collective.geo.opensearch')


def _parse_georss_box(value):
    try:
        lat0, lon0, lat1, lon1 = value.replace(',', ' ').split()
        # lat0, lon0
        # lowerLeft - the lower left coordinate. The latitude of this
        # point must be below the latitude of the upper right coordinate.
        # lat1, lon1
        # upperRight - the upper right coordinate. The latitude of this point
        # must be above the latitude of the lower left coordinate.
        if ((abs(int(float(lat0))) == 90) and (abs(int(float(lon0))) == 180) and
            (abs(int(float(lat1))) == 90) and (abs(int(float(lon1))) == 180)):
            # a bounding box comprising everything will not give us
            # additional information so we skip it
            return
        else:
            if float(lon0) < float(lon1):
                return {'type': 'Polygon', 'coordinates': ((
                                        (float(lon0), float(lat0)),
                                        (float(lon0), float(lat1)),
                                        (float(lon1), float(lat1)),
                                        (float(lon1), float(lat0)),
                                        (float(lon0), float(lat0)),
                        ),)}
            else:
                # the box crosses the dateline
                return {'type': 'MultiPolygon', 'coordinates': (
                                        ((float(lon0), float(lat0)),
                                        (float(lon0), float(lat1)),
                                        (-180.0, float(lat1)),
                                        (-180.0, float(lat0)),
                                        (float(lon0), float(lat0)),),
                                        ((180.0, float(lat0)),
                                        (180.0, float(lat1)),
                                        (float(lon1), float(lat1)),
                                        (float(lon1), float(lat0)),
                                        (180.0, float(lat0)),),
                                    )
                        }
    except Exception, e:
       logger.info('exeption raised in _parse_georss_box: %s' % e)



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
    #GeoRSS GML
    if 'georss_where' in entry:
        if (('gml_envelope' in entry) and ('gml_lowercorner' in entry) and
                ('gml_uppercorner') in entry):
            #XXX return smthng like a polygon
            # A bounding box defines a rectangular region. It is often
            # used to define the extents of a map or define a rough area
            # of interest. A GML box is called an Envelope. It consists
            # of an <Envelope> element with a child <lowerCorner> element
            # and a child <upperCorner> element.
            return _parse_georss_box(entry['gml_lowercorner'] + ' ' +
                        entry['gml_uppercorner'])
        elif ('gml_point' in entry) and ('gml_pos' in entry):
            # A point consists of a <Point> element with a child <pos> element.
            # Within <pos> the latitude and longitude values are separated by a space
            return _parse_georss_point(entry['gml_pos'])
        elif (('gml_polygon' in entry) and ('gml_exterior' in entry)
                and ('gml_linearring' in entry) and ('gml_poslist' in entry)):
            # A polygon consists of a <Polygon> element with a child <exterior>,
            # <LinearRing> and <posList> elements. There must be at least
            # four pairs with the last being identical to the first.
            # (a boundary has a minimum of three actual points.)
            # No two pairs may be separated by more than 179 degrees in
            # either latitude or longitude.
            return _parse_georss_polygon(entry['gml_poslist'])
        elif ('gml_linestring' in entry) and ('gml_poslist' in entry):
            # A line consists of a <LineString> element with a child <posList>
            # element. Within <posList> the coordinates of the points
            # on the line are entered as pairs of latitude and longitude
            # values, separated by spaces. There must be at least two pairs.
            # No two pairs may be separated by more than 179 degrees in
            # either latitude or longitude
            return _parse_georss_line(entry['gml_poslist'])
    # some versions of feedparser do not put the namespace in front :(
    elif 'where' in entry:
        if (('envelope' in entry) and ('lowercorner' in entry) and
                ('uppercorner') in entry):
            return _parse_georss_box(entry['lowercorner'] + ' ' +
                        entry['uppercorner'])
        elif ('point' in entry) and ('pos' in entry):
            # Point
            return _parse_georss_point(entry['pos'])
        elif (('polygon' in entry) and ('exterior' in entry)
                and ('linearring' in entry) and ('poslist' in entry)):
            # Polygon
            return _parse_georss_polygon(entry['poslist'])
        elif ('linestring' in entry) and ('poslist' in entry):
            # LineString
            return _parse_georss_line(entry['poslist'])
    #GeoRSS-Simple
    else:
        if 'georss_point' in entry:
            # A point contains a single latitude-longitude pair,
            # separated by whitespace.
            return _parse_georss_point(entry['georss_point'])
        elif 'georss_line' in entry:
            # A line contains a space separated list of latitude-longitude
            # pairs in WGS84 coordinate reference system, with each pair
            # separated by whitespace. There must be at least two pairs.
            return _parse_georss_line(entry['georss_line'])
        elif 'georss_polygon' in entry:
            # A polygon contains a space separated list of latitude-longitude
            # pairs, with each pair separated by whitespace. There must
            # be at least four pairs, with the last being identical to the
            # first (so a polygon has a minimum of three actual points).
            return _parse_georss_polygon(entry['georss_polygon'])
        elif 'georss_box' in entry:
            # A bounding box is a rectangular region, often used to define
            # the extents of a map or a rough area of interest. A box
            # contains two space seperate latitude-longitude pairs, with
            # each pair separated by whitespace. The first pair is the
            # lower corner, the second is the upper corner.
            return _parse_georss_box(entry['georss_box'])
        elif 'georss_circle' in entry:
            # A circle is a circular region containing three coordinates
            # (centerpoint latitude, centerpoint longitude, circle radius)
            # with latitude then longitude in the WGS84 coordinate reference
            # system and radius in meters.
            pass
        # some versions of feedparser do not put the namespace in front :(
        if 'point' in entry:
            return _parse_georss_point(entry['point'])
        elif 'line' in entry:
            return _parse_georss_line(entry['line'])
        elif 'polygon' in entry:
            return _parse_georss_polygon(entry['polygon'])
        elif 'box' in entry:
            return _parse_georss_box(entry['box'])
        elif 'circle' in entry:
            pass

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

