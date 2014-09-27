import json
import subprocess

import mercantile


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
        'echo "[-105, 39.99, -104.99, 40]" | mercantile tiles 14',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14]\n[3413, 6203, 14]'

def test_cli_tiles_bounding_tiles():
    result = subprocess.check_output(
        'echo "[-105, 39.99, -104.99, 40]" | mercantile tiles --bounding-tile',
        shell=True)
    assert result.decode('utf-8').strip() == '[1706, 3101, 13]'

def test_cli_tiles_bounding_tiles_z0():
    result = subprocess.check_output(
        'echo "[-1, -1, 1, 1]" | mercantile tiles --bounding-tile',
        shell=True)
    assert result.decode('utf-8').strip() == '[0, 0, 0]'

def test_cli_tiles_bounds():
    result = subprocess.check_output(
        'echo "[-105, 39.99, -104.99, 40]" | mercantile tiles 14 - --with-bounds',
        shell=True)
    first, last = result.decode('utf-8').strip().split('\n')
    assert [round(x, 3) for x in json.loads(first)][3:] == [-105.007, 39.994, -104.985, 40.011]


def test_cli_tiles_implicit_stdin():
    result = subprocess.check_output(
        'echo "[-105, 39.99, -104.99, 40]" | mercantile tiles 14',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14]\n[3413, 6203, 14]'


def test_cli_tiles_arg():
    result = subprocess.check_output(
        'mercantile tiles 14 "[-105, 39.99, -104.99, 40]"',
        shell=True)
    assert result.decode('utf-8').strip() == '[3413, 6202, 14]\n[3413, 6203, 14]'

def test_cli_tiles_geosjon():
    collection = {"features": [{"geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}
    result = subprocess.check_output(
        "echo '%s' | mercantile tiles 9" % json.dumps(collection),
        shell=True)
    result.decode('utf-8').strip() == '[]'


def test_cli_parent():
    result = subprocess.check_output(
        'echo "[486, 332, 10]\n[486, 332, 10]" | mercantile parent',
        shell=True)
    assert result.decode('utf-8').strip() == '[243, 166, 9]\n[243, 166, 9]'

def test_cli_grandparent():
    result = subprocess.check_output(
        'echo "[486, 332, 10]" | mercantile parent | mercantile parent',
        shell=True)
    assert result.decode('utf-8').strip() == '[121, 83, 8]'

def test_cli_parent_depth():
    result = subprocess.check_output(
        'echo "[486, 332, 10]" | mercantile parent --depth 2',
        shell=True)
    assert result.decode('utf-8').strip() == '[121, 83, 8]'


def test_cli_parent_multidepth():
    result = subprocess.check_output(
        'echo "[486, 332, 10]\n[121, 83, 8]" | mercantile parent --depth 2',
        shell=True)
    assert result.decode('utf-8').strip() == '[121, 83, 8]\n[30, 20, 6]'


def test_cli_children():
    result = subprocess.check_output(
        'echo "[243, 166, 9]" | mercantile children',
        shell=True)
    assert result.decode('utf-8').strip() == """
[486, 332, 10]
[487, 332, 10]
[487, 333, 10]
[486, 333, 10]
""".strip()


def test_cli_strict_overlap_contain():
    result = subprocess.check_output(
        'mercantile shapes "[2331,1185,12]" | mercantile tiles 12',
        shell=True)
    assert result.decode('utf-8').strip() == """
[2331, 1185, 12]
""".strip()
