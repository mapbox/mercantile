
import json

import mercantile


def open_output(arg):
    """Returns an opened output stream."""
    if arg == sys.stdout:
        return arg
    else:
        return open(arg, 'w')

def main(outfile, xyz):
    x, y, z = map(int, xyz.split(','))
    minlon, minlat, maxlon, maxlat = mercantile.bbox(x, y, z)
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
        json.dump(collection, sink)
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
    args = parser.parse_args()
    
    sys.exit(main(args.outfile, args.xyz))

