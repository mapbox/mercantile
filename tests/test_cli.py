"""Tests of the mercantile CLI"""

import json

from click.testing import CliRunner
import pytest

from mercantile.scripts import cli


def test_cli_shapes_failure():
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes"], "0")
    assert result.exit_code == 2


def test_cli_shapes():
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes", "--precision", "6"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )


def test_cli_shapes_arg():
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes", "[106, 193, 9]", "--precision", "6"])
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-105.46875, 39.909736, -104.765625, 40.446947], "geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )


def test_cli_shapes_buffer():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["shapes", "[106, 193, 9]", "--buffer", "1.0", "--precision", "6"]
    )
    assert result.exit_code == 0
    assert (
        result.output
        == '{"bbox": [-106.46875, 38.909736, -103.765625, 41.446947], "geometry": {"coordinates": [[[-106.46875, 38.909736], [-106.46875, 41.446947], [-103.765625, 41.446947], [-103.765625, 38.909736], [-106.46875, 38.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}\n'
    )


def test_cli_shapes_compact():
    """Output is compact."""
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes", "--compact"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert '"type":"Feature"' in result.output.strip()


def test_cli_shapes_indentation():
    """Output is indented."""
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes", "--indent", "8"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert '        "type": "Feature"' in result.output.strip()


def test_cli_shapes_collect():
    """Shapes are collected into a feature collection."""
    runner = CliRunner()
    result = runner.invoke(cli, ["shapes", "--collect", "--feature"], "[106, 193, 9]")
    assert result.exit_code == 0
    assert "FeatureCollection" in result.output


def test_cli_shapes_extents():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["shapes", "[106, 193, 9]", "--extents", "--mercator", "--precision", "3"]
    )
    assert result.exit_code == 0
    assert result.output == "-11740727.545 4852834.052 -11662456.028 4931105.569\n"


def test_cli_shapes_bbox():
    """JSON text sequences of bboxes are output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "shapes",
            "[106, 193, 9]",
            "--seq",
            "--bbox",
            "--mercator",
            "--precision",
            "3",
        ],
    )
    assert result.exit_code == 0
    assert (
        result.output
        == "\x1e\n[-11740727.545, 4852834.052, -11662456.028, 4931105.569]\n"
    )


def test_cli_shapes_props_fid():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "shapes",
            '{"tile": [106, 193, 9], "properties": {"title": "foo"}, "id": "42"}',
        ],
    )
    assert result.exit_code == 0
    assert '"title": "foo"' in result.output
    assert '"id": "42"' in result.output


def test_cli_tiles_bad_bounds():
    """Bounds of len 3 are bad."""
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[-105, 39.99, -104.99]")
    assert result.exit_code == 2


def test_cli_bounding_tile_bad_bounds():
    """Bounds of len 3 are bad."""
    runner = CliRunner()
    result = runner.invoke(cli, ["bounding-tile"], "[-105, 39.99, -104.99]")
    assert result.exit_code == 2


def test_cli_tiles_no_bounds():
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[-105, 39.99, -104.99, 40]")
    assert result.exit_code == 0
    assert result.output == "[3413, 6202, 14]\n[3413, 6203, 14]\n"


def test_cli_tiles_multi_bounds():
    """A LF-delimited sequence can be used as input."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["tiles", "14"], "[-105, 39.99, -104.99, 40]\n[-105, 39.99, -104.99, 40]"
    )
    assert result.exit_code == 0
    assert len(result.output.strip().split("\n")) == 4


def test_cli_tiles_multi_bounds_seq():
    """A JSON text sequence can be used as input."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["tiles", "14"],
        "\x1e\n[-105, 39.99, -104.99, 40]\n\x1e\n[-105, 39.99, -104.99, 40]",
    )
    assert result.exit_code == 0
    assert len(result.output.strip().split("\n")) == 4


def test_cli_bounding_tile():
    runner = CliRunner()
    result = runner.invoke(cli, ["bounding-tile"], "[-105, 39.99, -104.99, 40]")
    assert result.exit_code == 0
    assert result.output == "[1706, 3101, 13]\n"


def test_cli_bounding_tile_bbox():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["bounding-tile"], '{"bbox": [-105, 39.99, -104.99, 40]}'
    )
    assert result.exit_code == 0
    assert result.output == "[1706, 3101, 13]\n"


def test_cli_bounding_tile2():
    runner = CliRunner()
    result = runner.invoke(cli, ["bounding-tile"], "[-105, 39.99]")
    assert result.exit_code == 0


def test_cli_multi_bounding_tile():
    """A JSON text sequence can be used as input."""
    runner = CliRunner()
    result = runner.invoke(
        cli, ["bounding-tile"], "[-105, 39.99, -104.99, 40]\n[-105, 39.99, -104.99, 40]"
    )
    assert result.exit_code == 0
    assert len(result.output.strip().split("\n")) == 2


def test_cli_multi_bounding_tile_seq():
    """A JSON text sequence can be used as input."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["bounding-tile"],
        "\x1e\n[-105, 39.99, -104.99, 40]\n\x1e\n[-105, 39.99, -104.99, 40]",
    )
    assert result.exit_code == 0
    assert len(result.output.strip().split("\n")) == 2


def test_cli_tiles_bounding_tiles_z0():
    runner = CliRunner()
    result = runner.invoke(cli, ["bounding-tile"], "[-1, -1, 1, 1]")
    assert result.exit_code == 0
    assert result.output == "[0, 0, 0]\n"


def test_cli_tiles_bounding_tiles_seq():
    runner = CliRunner()
    result = runner.invoke(cli, ["bounding-tile", "--seq"], "[-1, -1, 1, 1]")
    assert result.exit_code == 0
    assert result.output == "\x1e\n[0, 0, 0]\n"


def test_cli_tiles_implicit_stdin():
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[-105, 39.99, -104.99, 40]")
    assert result.exit_code == 0
    assert result.output == "[3413, 6202, 14]\n[3413, 6203, 14]\n"


def test_cli_tiles_arg():
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14", "[-105, 39.99, -104.99, 40]"])
    assert result.exit_code == 0
    assert result.output == "[3413, 6202, 14]\n[3413, 6203, 14]\n"


def test_cli_tiles_geosjon():
    collection = '{"features": [{"geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "9"], collection)
    assert result.exit_code == 0
    assert result.output == "[106, 193, 9]\n[106, 194, 9]\n"


def test_cli_bounding_tile_geosjon():
    collection = '{"features": [{"geometry": {"coordinates": [[[-105.46875, 39.909736], [-105.46875, 40.446947], [-104.765625, 40.446947], [-104.765625, 39.909736], [-105.46875, 39.909736]]], "type": "Polygon"}, "id": "(106, 193, 9)", "properties": {"title": "XYZ tile (106, 193, 9)"}, "type": "Feature"}], "type": "FeatureCollection"}'
    runner = CliRunner()
    result = runner.invoke(cli, ["bounding-tile"], collection)
    assert result.exit_code == 0
    assert result.output == "[26, 48, 7]\n"


def test_cli_parent_failure():
    """[0, 0, 0] has no parent"""
    runner = CliRunner()
    result = runner.invoke(cli, ["parent"], "[0, 0, 0]")
    assert result.exit_code == 2


def test_cli_parent():
    runner = CliRunner()
    result = runner.invoke(cli, ["parent"], "[486, 332, 10]\n[486, 332, 10]")
    assert result.exit_code == 0
    assert result.output == "[243, 166, 9]\n[243, 166, 9]\n"


def test_cli_parent_depth():
    runner = CliRunner()
    result = runner.invoke(cli, ["parent", "--depth", "2"], "[486, 332, 10]")
    assert result.exit_code == 0
    assert result.output == "[121, 83, 8]\n"


def test_cli_parent_multidepth():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["parent", "--depth", "2"], "[486, 332, 10]\n[121, 83, 8]"
    )
    assert result.exit_code == 0
    assert result.output == "[121, 83, 8]\n[30, 20, 6]\n"


def test_cli_children():
    runner = CliRunner()
    result = runner.invoke(cli, ["children"], "[243, 166, 9]")
    assert result.exit_code == 0
    assert (
        result.output
        == "[486, 332, 10]\n[487, 332, 10]\n[487, 333, 10]\n[486, 333, 10]\n"
    )


def test_cli_neighbors():
    runner = CliRunner()
    result = runner.invoke(cli, ["neighbors"], "[243, 166, 9]")
    assert result.exit_code == 0

    tiles = result.output.strip().split("\n")
    tiles = [json.loads(t) for t in tiles]
    assert len(tiles) == 8

    # We do not provide ordering guarantees
    tiles = set([tuple(t) for t in tiles])

    assert (243, 166, 9) not in tiles, "input not in neighbors"

    assert (243 - 1, 166 - 1, 9) in tiles
    assert (243 - 1, 166 + 0, 9) in tiles
    assert (243 - 1, 166 + 1, 9) in tiles
    assert (243 + 0, 166 - 1, 9) in tiles
    assert (243 + 0, 166 + 1, 9) in tiles
    assert (243 + 1, 166 - 1, 9) in tiles
    assert (243 + 1, 166 + 0, 9) in tiles
    assert (243 + 1, 166 + 1, 9) in tiles


def test_cli_strict_overlap_contain():
    runner = CliRunner()
    result1 = runner.invoke(cli, ["shapes"], "[2331,1185,12]")
    assert result1.exit_code == 0
    result2 = runner.invoke(cli, ["tiles", "12"], result1.output)
    assert result2.exit_code == 0
    assert result2.output == "[2331, 1185, 12]\n"


def test_cli_tiles_seq():
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14", "--seq"], "[14.0859, 5.798]")
    assert result.exit_code == 0
    assert result.output == "\x1e\n[8833, 7927, 14]\n"


def test_cli_tiles_points():
    runner = CliRunner()
    result = runner.invoke(cli, ["tiles", "14"], "[14.0859, 5.798]")
    assert result.exit_code == 0
    assert result.output == "[8833, 7927, 14]\n"


def test_cli_tiles_point_geojson():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["tiles", "14"], '{"type":"geometry","coordinates":[14.0859, 5.798]}'
    )
    assert result.exit_code == 0
    assert result.output == "[8833, 7927, 14]\n"


def test_cli_quadkey_failure():
    """Abort when an invalid quadkey is passed"""
    runner = CliRunner()
    with pytest.warns(DeprecationWarning):
        result = runner.invoke(cli, ["quadkey", "lolwut"])
    assert result.exit_code == 2
    assert "lolwut" in result.output


def test_cli_quadkey_from_tiles():
    runner = CliRunner()
    result = runner.invoke(cli, ["quadkey"], "[486, 332, 10]\n[6826, 12415, 15]")
    assert result.exit_code == 0
    assert result.output == "0313102310\n023101012323232\n"


def test_cli_quadkey_from_quadkeys():
    runner = CliRunner()
    result = runner.invoke(cli, ["quadkey"], "0313102310\n023101012323232\n")
    assert result.exit_code == 0
    assert result.output == "[486, 332, 10]\n[6826, 12415, 15]\n"


def test_cli_quadkey_from_mixed():
    runner = CliRunner()
    result = runner.invoke(cli, ["quadkey"], "0313102310\n[6826, 12415, 15]\n")
    assert result.exit_code == 0
    assert result.output == "[486, 332, 10]\n023101012323232\n"
