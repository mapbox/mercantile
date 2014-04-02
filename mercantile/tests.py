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

