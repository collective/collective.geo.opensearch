#
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import shapely.geometry as geom

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
            upper_corner=coords[0][0:2]
            lower_corner=coords[0][2:4]
            return '\n'.join(template(
                            context,
                            upper='%f %f' % upper_corner,
                            lower='%f %f' % lower_corner
                        ).split('\n')[1:])
        else:
            raise ValueError, "Invalid dimensions"

