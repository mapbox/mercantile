import mercantile


def test_ul():
    expected = (-9.140625, 53.33087298301705)
    lnglat = mercantile.ul(486, 332, 10)
    for a, b in zip(expected, lnglat):
        assert round(a-b, 7) == 0
    assert lnglat[0] == lnglat.lng
    assert lnglat[1] == lnglat.lat


def test_bbox():
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    bbox = mercantile.bounds(486, 332, 10)
    for a, b in zip(expected, bbox):
        assert round(a-b, 7) == 0
    assert bbox.west == bbox[0]
    assert bbox.south == bbox[1]
    assert bbox.east == bbox[2]
    assert bbox.north == bbox[3]


def test_xy():
    ul = mercantile.ul(486, 332, 10)
    xy = mercantile.xy(*ul)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a-b, 7) == 0
    xy = mercantile.xy(0.0, 0.0)
    expected = (0.0, 0.0)
    for a, b in zip(expected, xy):
        assert round(a-b, 7) == 0


def test_tile():
    tile = mercantile.tile(20.6852, 40.1222, 9)
    expected = (285, 193)
    assert tile[0] == expected[0]
    assert tile[1] == expected[1]


def test_tiles():
    bounds = (-105, 39.99, -104.99, 40)
    tiles = list(mercantile.tiles(*bounds, zooms=[14]))
    expect = [mercantile.Tile(x=3413, y=6202, z=14),
              mercantile.Tile(x=3413, y=6203, z=14)]
    assert sorted(tiles) == sorted(expect)


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
