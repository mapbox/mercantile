"""Spherical mercator and XYZ tile utilities"""

# http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

from collections import namedtuple
import math


__all__ = ['ul', 'bounds', 'xy', 'tile']
__version__ = '0.2.1'

LngLat = namedtuple('LngLat', ['lng', 'lat'])
LngLatBbox = namedtuple('LngLatBbox', ['west', 'south', 'east', 'north'])

def ul(xtile, ytile, zoom):
    """Returns the upper left (lon, lat) of a tile"""
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return LngLat(lon_deg, lat_deg)

def bounds(xtile, ytile, zoom):
    """Returns the (lon, lat) bounding box of a tile"""
    a = ul(xtile, ytile, zoom)
    b = ul(xtile+1, ytile+1, zoom)
    return LngLatBbox(a[0], b[1], b[0], a[1])

def xy(lng, lat):
    """Returns the Spherical Mercator (x, y) in meters"""
    x = 6378137.0 * math.radians(lng)
    y = 6378137.0 * math.log(
        math.tan((math.pi*0.25) + (0.5 * math.radians(lat))) )
    return x, y

def tile(lng, lat, zoom):
    """Returns the (x, y) tile"""
    lat = math.radians(lat)
    n = 2.0 ** zoom
    xtile = int((lng + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(
        math.tan(lat) + (1 / math.cos(lat))) / math.pi) / 2.0 * n)
    return xtile, ytile

