import pytest

import mercantile


@pytest.mark.parametrize('args', [
    (486, 332, 10),
    [(486, 332, 10)],
    [mercantile.Tile(486, 332, 10)]])
def test_ul(args):
    expected = (-9.140625, 53.33087298301705)
    lnglat = mercantile.ul(*args)
    for a, b in zip(expected, lnglat):
        assert round(a - b, 7) == 0
    assert lnglat[0] == lnglat.lng
    assert lnglat[1] == lnglat.lat


@pytest.mark.parametrize('args', [
    (486, 332, 10),
    [(486, 332, 10)],
    [mercantile.Tile(486, 332, 10)]])
def test_bbox(args):
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    bbox = mercantile.bounds(*args)
    for a, b in zip(expected, bbox):
        assert round(a - b, 7) == 0
    assert bbox.west == bbox[0]
    assert bbox.south == bbox[1]
    assert bbox.east == bbox[2]
    assert bbox.north == bbox[3]


def test_xy():
    ul = mercantile.ul(486, 332, 10)
    xy = mercantile.xy(*ul)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0
    xy = mercantile.xy(0.0, 0.0)
    expected = (0.0, 0.0)
    for a, b in zip(expected, xy):
        assert round(a - b, 7) == 0


def test_xy_truncate():
    """Input is truncated"""
    assert mercantile.xy(-181.0, 0.0, truncate=True) == mercantile.xy(-180.0, 0.0)


def test_resolution():
    resolution = mercantile.resolution(0)
    initial_resolution = 20037508.342789244 * 2 / 256
    assert resolution == initial_resolution


def test_bounds_for_viewport():
    initial_resolution = 20037508.342789244 * 2 / 256
    bounds = mercantile.bounds_for_viewport(
        0, 45, 256, 256, initial_resolution
        )
    assert bounds == (
        (-180.0, 87.94905406387923), (180.0, -78.08802742575901)
    )


def test_lnglat():
    xy = (-1017529.7205322663, 7044436.526761846)
    lnglat = mercantile.lnglat(*xy)
    expected = (-9.140625, 53.33087298301705)
    for a, b in zip(expected, lnglat):
        assert round(a-b, 7) == 0


def test_tile():
    tile = mercantile.tile(20.6852, 40.1222, 9)
    expected = (285, 193)
    assert tile[0] == expected[0]
    assert tile[1] == expected[1]


def test_tile_truncate():
    """Input is truncated"""
    assert mercantile.tile(-181.0, 0.0, 9, truncate=True) == mercantile.tile(-180.0, 0.0, 9)


def test_tiles():
    bounds = (-105, 39.99, -104.99, 40)
    tiles = list(mercantile.tiles(*bounds, zooms=[14]))
    expect = [mercantile.Tile(x=3413, y=6202, z=14),
              mercantile.Tile(x=3413, y=6203, z=14)]
    assert sorted(tiles) == sorted(expect)


def test_tiles_truncate():
    """Input is truncated"""
    assert list(mercantile.tiles(-181.0, 0.0, -170.0, 10.0, zooms=[2], truncate=True)) \
        == list(mercantile.tiles(-180.0, 0.0, -170.0, 10.0, zooms=[2]))


def test_tiles_antimerdian_crossing_bbox():
    """Antimeridian-crossing bounding boxes are handled"""
    bounds = (175.0, 5.0, -175.0, 10.0)
    assert len(list(mercantile.tiles(*bounds, zooms=[2]))) == 2


def test_quadkey():
    tile = mercantile.Tile(486, 332, 10)
    expected = "0313102310"
    assert mercantile.quadkey(tile) == expected


def test_quadkey_to_tile():
    qk = "0313102310"
    expected = mercantile.Tile(486, 332, 10)
    assert mercantile.quadkey_to_tile(qk) == expected


def test_quadkey_failure():
    with pytest.raises(ValueError):
        mercantile.quadkey_to_tile('lolwut')


def test_parent():
    parent = mercantile.parent(486, 332, 10)
    assert parent == (243, 166, 9)
    assert parent.z == 9


def test_children():
    children = mercantile.children(243, 166, 9)
    assert len(children) == 4
    assert (486, 332, 10) in children


def test_bounding_tile():
    assert mercantile.bounding_tile(-92.5, 0.5, -90.5, 1.5) == (31, 63, 7)
    assert mercantile.bounding_tile(-90.5, 0.5, -89.5, 0.5) == (0, 0, 1)
    assert mercantile.bounding_tile(-92, 0, -88, 2) == (0, 0, 0)


def test_overflow_bounding_tile():
    assert mercantile.bounding_tile(
        -179.99999999999997,
        -90.00000000000003,
        180.00000000000014,
        -63.27066048950458) == (0, 0, 0)


def test_bounding_tile_pt():
    """A point is a valid input"""
    assert mercantile.bounding_tile(-91.5, 1.0).z == 28


def test_bounding_tile_truncate():
    """Input is truncated"""
    assert mercantile.bounding_tile(-181.0, 1.0, truncate=True) \
        == mercantile.bounding_tile(-180.0, 1.0)


def test_truncate_lng_under():
    assert mercantile.truncate_lnglat(-181, 0) == (-180, 0)


def test_truncate_lng_over():
    assert mercantile.truncate_lnglat(181, 0) == (180, 0)


def test_truncate_lat_under():
    assert mercantile.truncate_lnglat(0, -91) == (0, -90)


def test_truncate_lat_over():
    assert mercantile.truncate_lnglat(0, 91) == (0, 90)
