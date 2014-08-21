import subprocess

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

def test_cli_shapes():
    result = subprocess.check_output(
        'echo "[106, 193, 9]" | mercantile shapes - --precision 6',
        shell=True)
    assert result.decode('utf-8').strip() == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "features": [{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'


def test_cli_shapes_implicit_stdin():
    result = subprocess.check_output(
        'echo "[106, 193, 9]" | mercantile shapes --precision 6',
        shell=True)
    assert result.decode('utf-8').strip() == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "features": [{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'


def test_cli_shapes_arg():
    result = subprocess.check_output(
        'mercantile shapes "[106, 193, 9]" --precision 6',
        shell=True)
    assert result.decode('utf-8').strip() == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "features": [{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'

def test_cli_shapes_buffer():
    result = subprocess.check_output(
        'mercantile shapes "[106, 193, 9]" --buffer 1.0 --precision 6',
        shell=True)
    assert result.decode('utf-8').strip() == '{"bbox": [-106.46875, 38.909736, -103.765625, 41.446947], "features": [{"bbox": [-106.46875, 38.909736, -103.765625, 41.446947], "geometry": {"coordinates": [[[-106.46875, 38.909736], [-106.46875, 41.446947], [-103.765625, 41.446947], [-103.765625, 38.909736], [-106.46875, 38.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'

def test_cli_shapes_extents():
    result = subprocess.check_output(
        'mercantile shapes "[106, 193, 9]" --extents --mercator --precision 3',
        shell=True)
    assert result.decode('utf-8').strip() == '-11740727.545 4852834.052 -11662456.028 4931105.569'


def test_cli_tiles_no_bounds():
    result = subprocess.check_output(
        'echo "[-104.99, 39.99, -105, 40]" | mercantile tiles 14',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14]\n[3413, 6203, 14]'

def test_cli_tiles():
    result = subprocess.check_output(
        'echo "[-104.99, 39.99, -105, 40]" | mercantile tiles 14 - --bounds',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14, -105.00732421875, 39.9939556939733, -104.9853515625, 40.01078714046552]\n[3413, 6203, 14, -105.00732421875, 39.977120098439634, -104.9853515625, 39.9939556939733]'


def test_cli_tiles_implicit_stdin():
    result = subprocess.check_output(
        'echo "[-104.99, 39.99, -105, 40]" | mercantile tiles 14 --bounds',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14, -105.00732421875, 39.9939556939733, -104.9853515625, 40.01078714046552]\n[3413, 6203, 14, -105.00732421875, 39.977120098439634, -104.9853515625, 39.9939556939733]'


def test_cli_tiles_arg():
    result = subprocess.check_output(
        'mercantile tiles 14 "[-104.99, 39.99, -105, 40]" --bounds',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14, -105.00732421875, 39.9939556939733, -104.9853515625, 40.01078714046552]\n[3413, 6203, 14, -105.00732421875, 39.977120098439634, -104.9853515625, 39.9939556939733]'
