"""Spherical mercator and XYZ tile utilities"""

from collections import namedtuple
import math


__all__ = [
    'ul', 'bounds', 'xy', 'tile', 'parent', 'children', 'bounding_tile',
    'quadkey', 'quadkey_to_tile']
__version__ = '0.9.0'

Tile = namedtuple('Tile', ['x', 'y', 'z'])
LngLat = namedtuple('LngLat', ['lng', 'lat'])
LngLatBbox = namedtuple('LngLatBbox', ['west', 'south', 'east', 'north'])


def ul(*tile):
    """Returns the upper left (lon, lat) of a tile"""
    if len(tile) == 1:
        tile = tile[0]
    xtile, ytile, zoom = tile
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return LngLat(lon_deg, lat_deg)


def bounds(*tile):
    """Returns the (lon, lat) bounding box of a tile"""
    if len(tile) == 1:
        tile = tile[0]
    xtile, ytile, zoom = tile
    a = ul(xtile, ytile, zoom)
    b = ul(xtile + 1, ytile + 1, zoom)
    return LngLatBbox(a[0], b[1], b[0], a[1])


def truncate_lnglat(lng, lat):
    if lng > 180.0:
        lng = 180.0
    elif lng < -180.0:
        lng = -180.0
    if lat > 90.0:
        lat = 90.0
    elif lat < -90.0:
        lat = -90.0
    return lng, lat


def xy(lng, lat, truncate=False):
    """Returns the Spherical Mercator (x, y) in meters"""
    if truncate:
        lng, lat = truncate_lnglat(lng, lat)
    x = 6378137.0 * math.radians(lng)
    y = 6378137.0 * math.log(
        math.tan((math.pi * 0.25) + (0.5 * math.radians(lat))))
    return x, y


def tile(lng, lat, zoom, truncate=False):
    """Returns the (x, y, z) tile"""
    if truncate:
        lng, lat = truncate_lnglat(lng, lat)
    lat = math.radians(lat)
    n = 2.0 ** zoom
    try:
        xtile = int(math.floor((lng + 180.0) / 360.0 * n))
        ytile = int(math.floor((1.0 - math.log(
            math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * n))
    except ValueError:
        xtile = 0
        ytile = 0
    return Tile(xtile, ytile, zoom)


def quadkey(*tile):
    """Returns the quadkey of an (x, y, z) tile."""
    if len(tile) == 1:
        tile = tile[0]
    xtile, ytile, zoom = tile

    qk = []
    for z in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (z - 1)
        if xtile & mask:
            digit += 1
        if ytile & mask:
            digit += 2
        qk.append(str(digit))
    return ''.join(qk)


def quadkey_to_tile(qk):
    """Returns the (x, y, z) tile of the given quadkey."""
    xtile, ytile = 0, 0
    for i, digit in enumerate(reversed(qk)):
        mask = 1 << i
        if digit == '1':
            xtile = xtile | mask
        elif digit == '2':
            ytile = ytile | mask
        elif digit == '3':
            xtile = xtile | mask
            ytile = ytile | mask
        elif digit != '0':
            raise ValueError("Unexpected quadkey digit: %r", digit)
    return Tile(xtile, ytile, i + 1)


def tiles(west, south, east, north, zooms, truncate=False):
    """Yields the (x, y, z) tiles intersecting the bounding box."""
    if truncate:
        west, south = truncate_lnglat(west, south)
        east, north = truncate_lnglat(east, north)
    if west > east:
        bbox_west = (-180.0, south, east, north)
        bbox_east = (west, south, 180.0, north)
        bboxes = [bbox_west, bbox_east]
    else:
        bboxes = [(west, south, east, north)]
    for w, s, e, n in bboxes:
        for z in zooms:
            ll = tile(w, s, z)
            ur = tile(e, n, z)
            for i in range(ll.x, min(ur.x + 1, 2 ** z)):
                for j in range(ur.y, min(ll.y + 1, 2 ** z)):
                    yield Tile(i, j, z)


def parent(*tile):
    """Returns the parent of an (x, y, z) tile."""
    if len(tile) == 1:
        tile = tile[0]
    xtile, ytile, zoom = tile
    # Algorithm ported directly from https://github.com/mapbox/tilebelt.
    if xtile % 2 == 0 and ytile % 2 == 0:
        return Tile(xtile // 2, ytile // 2, zoom - 1)
    elif xtile % 2 == 0:
        return Tile(xtile // 2, (ytile - 1) // 2, zoom - 1)
    elif not xtile % 2 == 0 and ytile % 2 == 0:
        return Tile((xtile - 1) // 2, ytile // 2, zoom - 1)
    else:
        return Tile((xtile - 1) // 2, (ytile - 1) // 2, zoom - 1)


def children(*tile):
    """Returns the children of an (x, y, z) tile."""
    if len(tile) == 1:
        tile = tile[0]
    xtile, ytile, zoom = tile
    return [
        Tile(xtile * 2, ytile * 2, zoom + 1),
        Tile(xtile * 2 + 1, ytile * 2, zoom + 1),
        Tile(xtile * 2 + 1, ytile * 2 + 1, zoom + 1),
        Tile(xtile * 2, ytile * 2 + 1, zoom + 1)]


def rshift(val, n):
    return (val % 0x100000000) >> n


def bounding_tile(*bbox, **kwds):
    """Returns the smallest tile containing the bbox.

    NB: when the bbox spans lines of lng 0 or lat 0, the bounding tile
    will be (0, 0, 0)."""
    if len(bbox) == 2:
        bbox += bbox
    w, s, e, n = bbox
    truncate = bool(kwds.get('truncate'))
    if truncate:
        w, s = truncate_lnglat(w, s)
        e, n = truncate_lnglat(e, n)
    # Algorithm ported directly from https://github.com/mapbox/tilebelt.
    tmin = tile(w, s, 32, truncate=truncate)
    tmax = tile(e, n, 32, truncate=truncate)
    cell = tmin[:2] + tmax[:2]
    z = _getBboxZoom(*cell)
    if z == 0:
        return Tile(0, 0, 0)
    x = rshift(cell[0], (32 - z))
    y = rshift(cell[1], (32 - z))
    return Tile(x, y, z)


def _getBboxZoom(*bbox):
    MAX_ZOOM = 28
    for z in range(0, MAX_ZOOM):
        mask = 1 << (32 - (z + 1))
        if ((bbox[0] & mask) != (bbox[2] & mask)
                or (bbox[1] & mask) != (bbox[3] & mask)):
            return z
    return MAX_ZOOM
