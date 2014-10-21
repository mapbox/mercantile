"""Mercantile command line interface
"""

import json
import logging
import sys

import click

import mercantile


def configure_logging(verbosity):
    log_level = max(10, 30 - 10*verbosity)
    logging.basicConfig(stream=sys.stderr, level=log_level)


def coords(obj):
    """Yield all coordinate coordinate tuples from a geometry or feature.
    From python-geojson package."""
    if isinstance(obj, (tuple, list)):
        coordinates = obj
    elif 'geometry' in obj:
        coordinates = obj['geometry']['coordinates']
    else:
        coordinates = obj.get('coordinates', obj)
    for e in coordinates:
        if isinstance(e, (float, int)):
            yield tuple(coordinates)
            break
        else:
            for f in coords(e):
                yield f


# The CLI command group.
@click.group(help="Command line interface for the Mercantile Python package.")
@click.option('--verbose', '-v', count=True, help="Increase verbosity.")
@click.option('--quiet', '-q', count=True, help="Decrease verbosity.")
@click.pass_context
def cli(ctx, verbose, quiet):
    verbosity = verbose - quiet
    configure_logging(verbosity)
    ctx.obj = {}
    ctx.obj['verbosity'] = verbosity

# Commands are below.


# The shapes command.
@cli.command(short_help="Write the shapes of tiles as GeoJSON.")
# This input is either a filename, stdin, or a string.
@click.argument('input', default='-', required=False)
# Coordinate precision option.
@click.option('--precision', type=int, default=None,
              help="Decimal precision of coordinates.")
# JSON formatting options.
@click.option('--indent', default=None, type=int,
              help="Indentation level for JSON output")
@click.option('--compact/--no-compact', default=False,
              help="Use compact separators (',', ':').")
# Geographic (default) or Mercator switch.
@click.option('--geographic', 'projected', flag_value='geographic',
              default=True,
              help="Output in geographic coordinates (the default).")
@click.option('--mercator', 'projected', flag_value='mercator',
              help="Output in Web Mercator coordinates.")
# JSON object (default) or sequence switch.
@click.option('--json-obj', 'json_mode', flag_value='obj', default=True,
              help="Write a single JSON object (the default).")
@click.option('--x-json-seq', 'json_mode', flag_value='seq',
              help="Write a JSON sequence. Experimental.")
# Use ASCII RS control code to signal a sequence item (False is default).
# See http://tools.ietf.org/html/draft-ietf-json-text-sequence-05.
# Experimental.
@click.option('--x-json-seq-rs/--x-json-seq-no-rs', default=True,
              help="Use RS as text separator. Experimental.")
# GeoJSON feature (default) or collection switch. Meaningful only
# when --x-json-seq is used.
@click.option('--feature', 'output_mode', flag_value='feature',
              default=True,
              help="Output as sequence of GeoJSON features (the default).")
@click.option('--collection', 'output_mode', flag_value='collection',
              help="Output as sequence of GeoJSON feature collections.")
@click.option('--bbox', 'output_mode', flag_value='bbox',
              help="Output as sequence of GeoJSON bbox arrays.")
# Optionally write out bboxen in a form that goes
# straight into GDAL utilities like gdalwarp.
@click.option('--extents/--no-extents', default=False,
              help="Write shape extents as ws-separated strings (default is "
                   "False).")
# Optionally buffer the shapes by shifting the x and y values of each
# vertex by a constant number of decimal degrees or meters (depending
# on whether --geographic or --mercator is in effect).
@click.option('--buffer', type=float, default=None,
              help="Shift shape x and y values by a constant number")
@click.pass_context
def shapes(
        ctx, input, precision, indent, compact, projected,
        json_mode, x_json_seq_rs, output_mode, extents, buffer):

    """Reads one or more Web Mercator tile descriptions
    from stdin and writes either a GeoJSON feature collection (the
    default) or a JSON sequence of GeoJSON features/collections to
    stdout.

    tile descriptions may be either an [x, y, z] array or a JSON
    object of the form

      {"tile": [x, y, z], "properties": {"name": "foo", ...}}

    In the latter case, the properties object will be used to update
    the properties object of the output feature.
    """
    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('mercantile')
    dump_kwds = {'sort_keys': True}
    if indent:
        dump_kwds['indent'] = indent
    if compact:
        dump_kwds['separators'] = (',', ':')
    try:
        src = click.open_file(input).__iter__()
    except IOError:
        src = [input]
    stdout = click.get_text_stream('stdout')
    try:
        features = []
        col_xs = []
        col_ys = []
        for line in src:
            line = line.strip()
            obj = json.loads(line)
            if isinstance(obj, dict):
                x, y, z = obj['tile'][:3]
                props = obj['properties']
            elif isinstance(obj, list):
                x, y, z = obj[:3]
                props = {}
            else:
                raise ValueError("Invalid input: %r", obj)
            west, south, east, north = mercantile.bounds(x, y, z)
            if projected == 'mercator':
                west, south = mercantile.xy(west, south)
                east, north = mercantile.xy(east, north)
            if buffer:
                west -= buffer
                south -= buffer
                east += buffer
                north += buffer
            if precision and precision >= 0:
                west, south, east, north = (
                    round(v, precision) for v in (west, south, east, north))
            bbox = [
                min(west, east), min(south, north),
                max(west, east), max(south, north)]
            col_xs.extend([west, east])
            col_ys.extend([south, north])
            geom = {
                'type': 'Polygon',
                'coordinates': [[
                    [west, south],
                    [west, north],
                    [east, north],
                    [east, south],
                    [west, south]]]}
            xyz = str((x, y, z))
            feature = {
                'type': 'Feature',
                'bbox': bbox,
                'id': xyz,
                'geometry': geom,
                'properties': {'title': 'XYZ tile %s' % xyz}}
            if props:
                feature['properties'].update(props)
            if extents:
                stdout.write(" ".join(map(str, bbox)))
                stdout.write("\n")
            elif json_mode == 'seq':
                if x_json_seq_rs:
                    stdout.write(u'\u001e')
                if output_mode == 'bbox':
                    stdout.write(json.dumps(bbox, **dump_kwds))
                elif output_mode == 'feature':
                    stdout.write(json.dumps(feature, **dump_kwds))
                else:
                    stdout.write(json.dumps({
                        'type': 'FeatureCollection',
                        'features': [feature]}, **dump_kwds))
                stdout.write('\n')
            else:
                features.append(feature)
        if json_mode == 'obj' and not extents:
            bbox = [min(col_xs), min(col_ys), max(col_xs), max(col_ys)]
            stdout.write(json.dumps({
                'type': 'FeatureCollection',
                'bbox': bbox, 'features': features},
                **dump_kwds))
            stdout.write('\n')
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)


# The tiles command.
@cli.command(short_help="List tiles that overlap or contain a lng/lat point, "
                        "bounding box, or GeoJSON objects.")
# Mandatory Mercator zoom level argument.
@click.argument('zoom', type=int, default=-1)
# This input is either a filename, stdin, or a string.
# Has to follow the zoom arg.
@click.argument('input', default='-', required=False)
@click.option('--bounding-tile/--zoom-tiles', default=False)
# Optionally append [west, south, east, north] bounds of the tile to
# the output array.
@click.option('--with-bounds/--without-bounds', default=False,
              help="Append [w, s, e, n] tile bounds to output "
                   "(default is False).")
@click.option('--x-json-seq/--x-json-obj', default=False,
              help="Read a LF-delimited JSON sequence (default is object). "
                   "Experimental.")
@click.pass_context
def tiles(ctx, zoom, input, bounding_tile, with_bounds, x_json_seq):
    """Lists Web Mercator tiles at ZOOM level intersecting
    GeoJSON [west, south, east, north] bounding boxen, features, or
    collections read from stdin. Output is a JSON
    [x, y, z [, west, south, east, north -- optional]] array.

    Example:

    $ echo "[-105.05, 39.95, -105, 40]" | mercantile tiles 12

    Output:

    [852, 1550, 12]
    [852, 1551, 12]
    [853, 1550, 12]
    [853, 1551, 12]

    """
    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('mercantile')
    try:
        src = click.open_file(input).readlines()
    except IOError:
        src = [input]
    stdout = click.get_text_stream('stdout')

    src = iter(src)
    first_line = next(src)

    # If input is RS-delimited JSON sequence.
    if first_line.startswith(u'\x1e'):
        def feature_gen():
            buffer = first_line.strip(u'\x1e')
            for line in src:
                if line.startswith(u'\x1e'):
                    if buffer:
                        yield json.loads(buffer)
                    buffer = line.strip(u'\x1e')
                else:
                    buffer += line
            else:
                yield json.loads(buffer)
    elif x_json_seq:
        def feature_gen():
            yield json.loads(first_line)
            for line in src:
                yield json.loads(line)
    else:
        def feature_gen():
            logger.debug("Text a: %s", first_line)
            remainder = " ".join(list(src))
            logger.debug("Text b: %s", remainder)
            yield json.loads(first_line + remainder)

    try:
        source = feature_gen()
        # Detect the input format
        for obj in source:
            if isinstance(obj, list):
                bbox = obj
                if len(bbox) == 2:
                    bbox += bbox
                if len(bbox) != 4:
                    raise ValueError("Invalid input.")
            elif isinstance(obj, dict):
                if 'bbox' in obj:
                    bbox = obj['bbox']
                else:
                    box_xs = []
                    box_ys = []
                    for feat in obj.get('features', [obj]):
                        lngs, lats = zip(*list(coords(feat)))
                        box_xs.extend([min(lngs), max(lngs)])
                        box_ys.extend([min(lats), max(lats)])
                    bbox = min(box_xs), min(box_ys), max(box_xs), max(box_ys)
            west, south, east, north = bbox
            if bounding_tile:
                vals = mercantile.bounding_tile(west, south, east, north)
                output = json.dumps(vals)
                stdout.write(output)
                stdout.write('\n')
            else:
                # shrink the bounds a small amount so that
                # shapes/tiles round trip.
                west += 1.0e-10
                south += 1.0e-10
                east -= 1.0e-10
                north -= 1.0e-10
                minx, miny, _ = mercantile.tile(west, north, zoom)
                maxx, maxy, _ = mercantile.tile(east, south, zoom)
                logger.debug("Tile ranges [%d:%d, %d:%d]",
                             minx, maxx, miny, maxy)
                for x in range(minx, maxx+1):
                    for y in range(miny, maxy+1):
                        vals = (x, y, zoom)
                        if with_bounds:
                            vals += mercantile.bounds(x, y, zoom)
                        output = json.dumps(vals)
                        stdout.write(output)
                        stdout.write('\n')
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)


# The children command.
@cli.command(short_help="Write the children of the tile.")
@click.argument('input', default='-', required=False)
@click.option('--depth', type=int, default=1,
              help="Number of zoom levels to traverse (default is 1).")
@click.pass_context
def children(ctx, input, depth):
    """Takes a [x, y, z] tile as input and writes its children to stdout
    in the same form.

    $ echo "[486, 332, 10]" | mercantile parent

    Output:

    [243, 166, 9]
    """
    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('mercantile')
    try:
        src = click.open_file(input).readlines()
    except IOError:
        src = [input]
    stdout = click.get_text_stream('stdout')

    try:
        for line in src:
            line = line.strip()
            tiles = [json.loads(line)[:3]]
            for i in range(depth):
                tiles = sum([mercantile.children(t) for t in tiles], [])
            for t in tiles:
                output = json.dumps(t)
                stdout.write(output)
                stdout.write('\n')
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)


# The parent command.
@cli.command(short_help="Write the parent tile.")
@click.argument('input', default='-', required=False)
@click.option('--depth', type=int, default=1,
              help="Number of zoom levels to traverse (default is 1).")
@click.pass_context
def parent(ctx, input, depth):
    """Takes a [x, y, z] tile as input and writes its parent to stdout
    in the same form.

    $ echo "[486, 332, 10]" | mercantile parent

    Output:

    [243, 166, 9]
    """
    verbosity = ctx.obj['verbosity']
    logger = logging.getLogger('mercantile')
    try:
        src = click.open_file(input).readlines()
    except IOError:
        src = [input]
    stdout = click.get_text_stream('stdout')

    try:
        for line in src:
            line = line.strip()
            tile = json.loads(line)[:3]
            if tile[2] - depth < 0:
                raise ValueError("Maximum depth exceeded.")
            for i in range(depth):
                tile = mercantile.parent(tile)
            output = json.dumps(tile)
            stdout.write(output)
            stdout.write('\n')
        sys.exit(0)
    except Exception:
        logger.exception("Failed. Exception caught")
        sys.exit(1)
