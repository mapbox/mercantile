import warnings

from hypothesis import example, given
from hypothesis.strategies import composite, integers
import pytest

import mercantile


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [mercantile.Tile(486, 332, 10)]]
)
def test_ul(args):
    expected = (-9.140625, 53.33087298301705)
    lnglat = mercantile.ul(*args)
    for a, b in zip(expected, lnglat):
        assert round(a - b, 7) == 0
    assert lnglat[0] == lnglat.lng
    assert lnglat[1] == lnglat.lat


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [mercantile.Tile(486, 332, 10)]]
)
def test_bbox(args):
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    bbox = mercantile.bounds(*args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 7) == 0
    assert bbox.west == bbox[0]
    assert bbox.south == bbox[1]
    assert bbox.east == bbox[2]
    assert bbox.north == bbox[3]


def test_xy_tile():
    """x, y for the 486-332-10 tile is correctly calculated"""
    ul = mercantile.ul(486, 332, 10)
    xy = mercantile.xy(*ul)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_xy_null_island():
    """x, y for (0, 0) is correctly calculated"""
    xy = mercantile.xy(0.0, 0.0)
    expected = (0.0, 0.0)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_xy_south_pole():
    """Return -inf for y at South Pole"""
    assert mercantile.xy(0.0, -90) == (0.0, float("-inf"))


def test_xy_north_pole():
    """Return inf for y at North Pole"""
    assert mercantile.xy(0.0, 90) == (0.0, float("inf"))


def test_xy_truncate():
    """Input is truncated"""
    assert mercantile.xy(-181.0, 0.0, truncate=True) == mercantile.xy(-180.0, 0.0)


def test_lnglat():
    xy = (-8366731.739810849, -1655181.9927159143)
    assert mercantile.lnglat(*xy) == (-75.15963, -14.704620000000013)


def test_lnglat_truncate():
    xy = (-28366731.739810849, -1655181.9927159143)
    assert mercantile.lnglat(*xy, truncate=True) == (-180, -14.704620000000013)


def test_lnglat_xy_roundtrip():
    lnglat = (-105.0844, 40.5853)
    roundtrip = mercantile.lnglat(*mercantile.xy(*lnglat))
    for a, b in zip(roundtrip, lnglat):
        assert round(a - b, 7) == 0


@pytest.mark.parametrize(
    "args", [(486, 332, 10), [(486, 332, 10)], [mercantile.Tile(486, 332, 10)]]
)
def test_xy_bounds(args):
    expected = (
        -1017529.7205322663,
        7005300.768279833,
        -978393.962050256,
        7044436.526761846,
    )
    bounds = mercantile.xy_bounds(*args)

    for a, b in zip(expected, bounds):
        assert round(a - b, 7) == 0


def test_tile_not_truncated():
    tile = mercantile.tile(20.6852, 40.1222, 9)
    expected = (285, 193)
    assert tile[0] == expected[0]
    assert tile[1] == expected[1]


def test_tile_truncate():
    """Input is truncated"""
    assert mercantile.tile(-181.0, 0.0, 9, truncate=True) == mercantile.tile(
        -180.0, 0.0, 9
    )


def test_tiles():
    bounds = (-105, 39.99, -104.99, 40)
    tiles = list(mercantile.tiles(*bounds, zooms=[14]))
    expect = [
        mercantile.Tile(x=3413, y=6202, z=14),
        mercantile.Tile(x=3413, y=6203, z=14),
    ]
    assert sorted(tiles) == sorted(expect)


def test_tiles_single_zoom():
    bounds = (-105, 39.99, -104.99, 40)
    tiles = list(mercantile.tiles(*bounds, zooms=14))
    expect = [
        mercantile.Tile(x=3413, y=6202, z=14),
        mercantile.Tile(x=3413, y=6203, z=14),
    ]
    assert sorted(tiles) == sorted(expect)


def test_tiles_truncate():
    """Input is truncated"""
    assert list(
        mercantile.tiles(-181.0, 0.0, -170.0, 10.0, zooms=[2], truncate=True)
    ) == list(mercantile.tiles(-180.0, 0.0, -170.0, 10.0, zooms=[2]))


def test_tiles_antimerdian_crossing_bbox():
    """Antimeridian-crossing bounding boxes are handled"""
    bounds = (175.0, 5.0, -175.0, 10.0)
    assert len(list(mercantile.tiles(*bounds, zooms=[2]))) == 2


def test_global_tiles_clamped():
    """Y is clamped to (0, 2 ** zoom - 1)"""
    tiles = list(mercantile.tiles(-180, -90, 180, 90, [1]))
    assert len(tiles) == 4
    assert min(t.y for t in tiles) == 0
    assert max(t.y for t in tiles) == 1


@pytest.mark.parametrize(
    "t",
    [
        mercantile.Tile(x=3413, y=6202, z=14),
        mercantile.Tile(486, 332, 10),
        mercantile.Tile(10, 10, 10),
    ],
)
def test_tiles_roundtrip(t):
    """tiles(bounds(tile)) gives the tile"""
    res = list(mercantile.tiles(*mercantile.bounds(t), zooms=[t.z]))
    assert len(res) == 1
    val = res.pop()
    assert val.x == t.x
    assert val.y == t.y
    assert val.z == t.z


def test_tiles_roundtrip_children():
    """tiles(bounds(tile)) gives the tile's children"""
    t = mercantile.Tile(x=3413, y=6202, z=14)
    res = list(mercantile.tiles(*mercantile.bounds(t), zooms=[15]))
    assert len(res) == 4


def test_quadkey():
    tile = mercantile.Tile(486, 332, 10)
    expected = "0313102310"
    assert mercantile.quadkey(tile) == expected


def test_quadkey_to_tile():
    qk = "0313102310"
    expected = mercantile.Tile(486, 332, 10)
    assert mercantile.quadkey_to_tile(qk) == expected


def test_empty_quadkey_to_tile():
    qk = ""
    expected = mercantile.Tile(0, 0, 0)
    assert mercantile.quadkey_to_tile(qk) == expected


def test_quadkey_failure(recwarn):
    """expect a deprecation warning"""
    warnings.simplefilter("always")
    with pytest.raises(mercantile.QuadKeyError):
        mercantile.quadkey_to_tile("lolwut")
    assert len(recwarn) == 1
    assert recwarn.pop(DeprecationWarning)


def test_root_parent():
    assert mercantile.parent(0, 0, 0) is None


@pytest.mark.parametrize("args", [(486, 332, 10, 9), ((486, 332, 10), 9)])
def test_parent_invalid_args(args):
    """tile arg must have length 1 or 3"""
    with pytest.raises(mercantile.TileArgParsingError):
        mercantile.parent(*args)


def test_parent():
    parent = mercantile.parent(486, 332, 10)
    assert parent == (243, 166, 9)
    assert parent.z == 9


def test_parent_multi():
    parent = mercantile.parent(486, 332, 10, zoom=8)
    assert parent == (121, 83, 8)
    assert parent.z == 8


def test_children():
    x, y, z = 243, 166, 9
    children = mercantile.children(x, y, z)
    assert len(children) == 4

    # Four sub-tiles (children) when zooming in
    #
    #    -------
    #   | a | b |
    #    ---|---
    #   | d | c |
    #    -------
    #
    # with:
    #
    #   a=(2x,     2y, z + 1)    b=(2x + 1,     2y, z + 1)
    #
    #   d=(2x, 2y + 1, z + 1)    c=(2x + 1, 2y + 1, z + 1)
    #
    # See: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Subtiles

    a, b, c, d = children

    assert a == mercantile.Tile(2 * x, 2 * y, z + 1)
    assert b == mercantile.Tile(2 * x + 1, 2 * y, z + 1)
    assert c == mercantile.Tile(2 * x + 1, 2 * y + 1, z + 1)
    assert d == mercantile.Tile(2 * x, 2 * y + 1, z + 1)


def test_children_multi():
    children = mercantile.children(243, 166, 9, zoom=11)
    assert len(children) == 16
    targets = [
        (972, 664, 11),
        (973, 664, 11),
        (973, 665, 11),
        (972, 665, 11),
        (974, 664, 11),
        (975, 664, 11),
        (975, 665, 11),
        (974, 665, 11),
        (974, 666, 11),
        (975, 666, 11),
        (975, 667, 11),
        (974, 667, 11),
        (972, 666, 11),
        (973, 666, 11),
        (973, 667, 11),
        (972, 667, 11),
    ]
    for target in targets:
        assert target in children


def test_child_fractional_zoom():
    with pytest.raises(mercantile.InvalidZoomError) as e:
        mercantile.children((243, 166, 9), zoom=10.2)
    assert "zoom must be an integer and greater than" in str(e.value)


def test_child_bad_tile_zoom():
    with pytest.raises(mercantile.InvalidZoomError) as e:
        mercantile.children((243, 166, 9), zoom=8)
    assert "zoom must be an integer and greater than" in str(e.value)


def test_parent_fractional_tile():
    with pytest.raises(mercantile.ParentTileError) as e:
        mercantile.parent((243.3, 166.2, 9), zoom=1)
    assert "the parent of a non-integer tile is undefined" in str(e.value)


def test_parent_fractional_zoom():
    with pytest.raises(mercantile.InvalidZoomError) as e:
        mercantile.parent((243, 166, 9), zoom=1.2)
    assert "zoom must be an integer and less than" in str(e.value)


def test_parent_bad_tile_zoom():
    with pytest.raises(mercantile.InvalidZoomError) as e:
        mercantile.parent((243.3, 166.2, 9), zoom=10)
    assert "zoom must be an integer and less than" in str(e.value)


def test_neighbors():
    x, y, z = 243, 166, 9
    tiles = mercantile.neighbors(x, y, z)
    assert len(tiles) == 8
    assert all(t.z == z for t in tiles)
    assert all(t.x - x in (-1, 0, 1) for t in tiles)
    assert all(t.y - y in (-1, 0, 1) for t in tiles)


def test_neighbors_invalid():
    x, y, z = 0, 166, 9
    tiles = mercantile.neighbors(x, y, z)
    assert len(tiles) == 8 - 3  # no top-left, left, bottom-left
    assert all(t.z == z for t in tiles)
    assert all(t.x - x in (-1, 0, 1) for t in tiles)
    assert all(t.y - y in (-1, 0, 1) for t in tiles)


def test_root_neighbors_invalid():
    x, y, z = 0, 0, 0
    tiles = mercantile.neighbors(x, y, z)
    assert len(tiles) == 0  # root tile has no neighbors


def test_simplify():
    children = mercantile.children(243, 166, 9, zoom=12)
    assert len(children) == 64
    children = children[:-3]
    children.append(children[0])
    simplified = mercantile.simplify(children)
    targets = [
        (487, 332, 10),
        (486, 332, 10),
        (487, 333, 10),
        (973, 667, 11),
        (973, 666, 11),
        (972, 666, 11),
        (1944, 1334, 12),
    ]
    for target in targets:
        assert target in simplified


def test_simplify_removal():
    ''' Verify that tiles are being removed by simplify()
    '''
    tiles = [
        (1298, 3129, 13),
        (649, 1564, 12),
        (650, 1564, 12),
        ]
    simplified = mercantile.simplify(tiles)
    assert (1298, 3129, 13) not in simplified, 'Tile covered by a parent'
    assert (650, 1564, 12) in simplified, 'Highest-level tile'
    assert (649, 1564, 12) in simplified, 'Also highest-level tile'


@pytest.mark.parametrize(
    "bounds,tile",
    [
        ((-92.5, 0.5, -90.5, 1.5), (31, 63, 7)),
        ((-90.5, 0.5, -89.5, 0.5), (0, 0, 1)),
        ((-92, 0, -88, 2), (0, 0, 1)),
        ((-92, -2, -88, 2), (0, 0, 0)),
        ((-92, -2, -88, 0), (0, 1, 1)),
    ],
)
def test_bounding_tile(bounds, tile):
    assert mercantile.bounding_tile(*bounds) == mercantile.Tile(*tile)


def test_overflow_bounding_tile():
    assert mercantile.bounding_tile(
        -179.99999999999997, -90.00000000000003, 180.00000000000014, -63.27066048950458
    ) == (0, 0, 0)


def test_bounding_tile_pt():
    """A point is a valid input"""
    assert mercantile.bounding_tile(-91.5, 1.0).z == 28


def test_bounding_tile_truncate():
    """Input is truncated"""
    assert mercantile.bounding_tile(
        -181.0, 1.0, truncate=True
    ) == mercantile.bounding_tile(-180.0, 1.0)


def test_truncate_lng_under():
    assert mercantile.truncate_lnglat(-181, 0) == (-180, 0)


def test_truncate_lng_over():
    assert mercantile.truncate_lnglat(181, 0) == (180, 0)


def test_truncate_lat_under():
    assert mercantile.truncate_lnglat(0, -91) == (0, -90)


def test_truncate_lat_over():
    assert mercantile.truncate_lnglat(0, 91) == (0, 90)


@pytest.mark.parametrize(
    "args, tile",
    [
        ((0, 0, 0), (0, 0, 0)),
        (mercantile.Tile(0, 0, 0), (0, 0, 0)),
        (((0, 0, 0)), (0, 0, 0)),
    ],
)
def test_arg_parse(args, tile):
    """Helper function parse tile args properly"""
    assert mercantile._parse_tile_arg(*args) == mercantile.Tile(*tile)


@pytest.mark.parametrize("args", [(0, 0), (0, 0, 0, 0)])
def test_arg_parse_error(args):
    """Helper function raises exception as expected"""
    with pytest.raises(mercantile.TileArgParsingError):
        mercantile._parse_tile_arg(*args)


@composite
def tiles(draw, zooms=integers(min_value=0, max_value=28)):
    z = draw(zooms)
    x = draw(integers(min_value=0, max_value=2 ** z - 1))
    y = draw(integers(min_value=0, max_value=2 ** z - 1))
    return mercantile.Tile(x, y, z)


@given(tiles())
@example(mercantile.Tile(10, 10, 10))
def test_bounding_tile_roundtrip(t):
    """bounding_tile(bounds(tile)) gives the tile"""
    val = mercantile.bounding_tile(*mercantile.bounds(t))
    assert val.x == t.x
    assert val.y == t.y
    assert val.z == t.z


@given(tiles())
@example(mercantile.Tile(10, 10, 10))
def test_ul_tile_roundtrip(t):
    """ul and tile roundtrip"""
    lnglat = mercantile.ul(t)
    tile = mercantile.tile(lnglat.lng, lnglat.lat, t.z)
    assert tile.z == t.z
    assert tile.x == t.x
    assert tile.y == t.y


@given(tiles())
@example(mercantile.Tile(10, 10, 10))
def test_ul_xy_bounds(t):
    """xy(*ul(t)) will be within 1e-7 of xy_bounds(t)"""
    assert mercantile.xy(*mercantile.ul(t))[1] == pytest.approx(
        mercantile.xy_bounds(t).top, abs=1e-7
    )
    assert mercantile.xy(*mercantile.ul(t))[0] == pytest.approx(
        mercantile.xy_bounds(t).left, abs=1e-7
    )


def test_lower_left_tile():
    assert mercantile.tile(180.0, -85, 1) == mercantile.Tile(1, 1, 1)


@pytest.mark.parametrize("lat", [-90.0, 90.0])
def test_tile_poles(lat):
    with pytest.raises(mercantile.InvalidLatitudeError):
        mercantile.tile(0.0, lat, zoom=17)


@pytest.mark.parametrize("lat", [-90.0, 90.0])
def test__xy_poles(lat):
    with pytest.raises(mercantile.InvalidLatitudeError):
        mercantile._xy(0.0, lat)


@pytest.mark.parametrize("lat,fy", [(85.0511287798066, 0.0), (-85.0511287798066, 1.0)])
def test__xy_limits(lat, fy):
    x, y = mercantile._xy(0.0, lat)
    assert x == 0.5
    assert y == pytest.approx(fy)


@pytest.mark.parametrize("lat", [86.0])
def test__xy_north_of_limit(lat):
    x, y = mercantile._xy(0.0, lat)
    assert x == 0.5
    assert y < 0


@pytest.mark.parametrize("lat", [-86.0])
def test__xy_south_of_limit(lat):
    x, y = mercantile._xy(0.0, lat)
    assert x == 0.5
    assert y > 1


def test_minmax():
    """Exercise minmax from zoom levels 0 to 28"""
    assert mercantile.minmax(zoom=0) == (0, 0)
    assert mercantile.minmax(zoom=1) == (0, 1)

    for z in range(0, 28):
        minimum, maximum = mercantile.minmax(z)

        assert minimum == 0
        assert maximum >= 0
        assert maximum == 2 ** z - 1


@pytest.mark.parametrize("z", [1.2, "lol", -1])
def test_minmax_error(z):
    """Get an exception when zoom is invalid"""
    with pytest.raises(mercantile.InvalidZoomError):
        mercantile.minmax(z)


@pytest.mark.parametrize(
    "obj",
    [
        {"features": [{"geometry": {"coordinates": (1, 2)}}]},
        {"geometry": {"coordinates": (1, 2)}},
        {"coordinates": (1, 2)},
        {"coordinates": [(1, 2)]},
        (1, 2),
        [(1, 2)],
    ],
)
def test_coords(obj):
    """Get coordinates of mock geojson objects"""
    assert list(mercantile._coords(obj)) == [(1, 2)]


@pytest.mark.parametrize(
    "obj",
    [
        {
            "features": [
                {"geometry": {"coordinates": (1, 2)}},
                {"geometry": {"coordinates": (-1, -2)}},
            ]
        },
        {"geometry": {"coordinates": [(1, 2), (-1, -2)]}},
        {"coordinates": [(1, 2), (-1, -2)]},
        [(1, 2), (-1, -2)],
    ],
)
def test_geojson_bounds(obj):
    """Get bounds of mock geojson objects"""
    bbox = mercantile.geojson_bounds(obj)
    assert bbox.west == -1.0
    assert bbox.south == -2.0
    assert bbox.east == 1.0
    assert bbox.north == 2.0


@pytest.mark.parametrize("x,y", [(0, 1), (1, 0), (-1, 0), (0, -1)])
def test_xy_future_warnings(x, y):
    with pytest.warns(FutureWarning):
        mercantile.Tile(x, y, 0)
