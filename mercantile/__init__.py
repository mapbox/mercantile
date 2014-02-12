"""Spherical mercator and XYZ tile utilities"""

# http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

import math


def ul(xtile, ytile, zoom):
    """Returns the upper left (lon, lat) of a tile"""
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lon_deg, lat_deg)

def bbox(xtile, ytile, zoom):
    """Returns the (lon, lat) bounding box of a tile"""
    a = ul(xtile, ytile, zoom)
    b = ul(xtile+1, ytile+1, zoom)
    return (a[0], b[1], b[0], a[1])

def xy(lon, lat):
    """Returns the Spherical Mercator (x, y) in meters"""
    x = 6378137.0 * math.radians(lon)
    y = 6378137.0 * math.log(
        math.tan((math.pi*0.25) + (0.5 * math.radians(53.33087298301705))) )
    return x, y

