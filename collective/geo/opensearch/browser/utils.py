#
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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
        elif brain.zgeo_geometry['type'] in ['MultiPoint',
                            'MultiLineString', 'MultiPolygon']
            pass
            #XXX do something resonable here, maybe just return the bounding box
            # or a polygon that outlines all coordinates
            # shapely.geometry.MultiLineString(brain.zgeo_geometry['coordinates']).convex_hull.to_wkt()
            # .bounds or .envelope
            # A bounding box defines a rectangular region.
            # It is often used to define the extents of a map or define a
            # rough area of interest. A GML box is called an Envelope.
            return
        else:
            raise ValueError, "Invalid geometry type"
        if len(coords[0]) == 2 or len(coords[0]) == 3:
            tuples = ('%f %f' % (c[1], c[0]) for c in coords)
        else:
            raise ValueError, "Invalid dimensions"
        return '\n'.join(template(context, coords=' '.join(tuples)).split('\n')[1:])
