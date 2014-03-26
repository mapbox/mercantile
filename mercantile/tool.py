""" mercantile.tool

Writes extents of XYZ tiles to GeoJSON.
"""

import json

import mercantile


def open_output(arg):
    """Returns an opened output stream."""
    if arg == sys.stdout:
        return arg
    else:
        return open(arg, 'w')

def main(outfile, xyz, **dump_kw):
    x, y, z = map(int, xyz.split(','))
    minlon, minlat, maxlon, maxlat = (
            round(v, 6) for v in mercantile.bounds(x, y, z))
    
    geom = {
        'type': 'Polygon',
        'coordinates': [[
            [minlon, minlat],
            [minlon, maxlat],
            [maxlon, maxlat],
            [maxlon, minlat],
            [minlon, minlat] ]]}
    feature = {
        'type': 'Feature',
        'id': xyz,
        'geometry': geom,
        'properties': {'title': 'XYZ tile %s' % xyz} }
    collection = {'type': 'FeatureCollection', 'features': [feature]}
    
    with open_output(args.outfile) as sink:
        json.dump(collection, sink, **dump_kw)
    
    return 0

if __name__ == '__main__':

    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Write the footprint of an XYZ tile to GeoJSON")
    parser.add_argument(
        'xyz',
        metavar='X,Y,Z',
        help="Tile coordinates")
    parser.add_argument(
        'outfile',
        nargs='?', 
        help="output file name, defaults to stdout if omitted", 
        default=sys.stdout)
    parser.add_argument('-n', '--indent', 
        type=int,
        default=None,
        metavar='N',
        help="indentation level in N number of chars")
    parser.add_argument('--compact', 
        action='store_true',
        help="use compact separators (',', ':')")
    parser.add_argument('--pretty', 
        action='store_true',
        help="Pretty print with indentation level of 2 chars")

    args = parser.parse_args()
    
    # Keyword args to be used in all following json.dump* calls.
    dump_kw = {'sort_keys': True}
    if args.pretty:
        dump_kw['indent'] = 2
    if args.indent:
        dump_kw['indent'] = args.indent
    if args.compact:
        dump_kw['separators'] = (',', ':')


    sys.exit(main(args.outfile, args.xyz, **dump_kw))

