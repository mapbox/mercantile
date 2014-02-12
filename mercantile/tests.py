import mercantile

def test_ul():
    expected = (-9.140625, 53.33087298301705)
    lonlat = mercantile.ul(486, 332, 10)
    for a, b in zip(expected, lonlat):
        assert round(a-b, 7) == 0

def test_bbox():
    expected = (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    bbox = mercantile.bbox(486, 332, 10)
    for a, b in zip(expected, bbox):
        assert round(a-b, 7) == 0

def test_xy():
    ul = mercantile.ul(486, 332, 10)
    xy = mercantile.xy(*ul)
    expected = (-1017529.7205322663, 7044436.526761846)
    for a, b in zip(expected, xy):
        assert round(a-b, 7) == 0
