==========
Mercantile
==========

Spherical mercator coordinate and tile utilities

The mercantile module provides ``ul(xtile, ytile, zoom)`` and ``bounds(xtile,
ytile, zoom)`` functions that return longitudes and latitudes for XYZ tiles,
and a ``xy(lon, lat)`` function that returns spherical mercator x and
y coordinates.

.. code-block:: pycon

    >>> import mercantile
    >>> mercantile.ul(486, 332, 10)
    (-9.140625, 53.33087298301705)
    >>> mercantile.bounds(486, 332, 10)
    (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    >>> mercantile.xy(*mercantile.ul(486, 332, 10))
    (-1017529.7205322663, 7044436.526761846)

Mercantile CLI
==============

Mercantile's command line interface, named "mercantile", has commands for 
getting the shapes of Web Mercator tiles as GeoJSON and getting the tiles
that intersect with a GeoJSON bounding box. 

.. code-block:: console

    $ mercantile --help
    Usage: mercantile [OPTIONS] COMMAND [ARGS]...

      Mercantile command line interface.

    Options:
      -v, --verbose  Increase verbosity.
      -q, --quiet    Decrease verbosity.
      --help         Show this message and exit.

    Commands:
      shapes  Write the shapes of tiles as GeoJSON.
      tiles   List tiles intersecting a lng/lat bounding box.


shapes
------

The shapes command writes Mercator tile shapes to several forms of GeoJSON.

.. code-block:: 

    $ echo "[106, 193, 9]" | mercantile shapes - --indent 2 --precision 6
    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  -105.46875,
                  39.909736
                ],
                [
                  -105.46875,
                  40.446947
                ],
                [
                  -104.765625,
                  40.446947
                ],
                [
                  -104.765625,
                  39.909736
                ],
                [
                  -105.46875,
                  39.909736
                ]
              ]
            ],
            "type": "Polygon"
          },
          "id": "(106, 193, 9)",
          "properties": {
            "title": "XYZ tile (106, 193, 9)"
          },
          "type": "Feature"
        }
      ],
      "type": "FeatureCollection"
    }

tiles
-----

The tiles command writes descriptions of tiles intersecting with a geographic
bounding box.

.. code-block:: console

    $ echo "[-104.99, 39.99, -105, 40]" | mercantile tiles - 14
    [3413, 6202, 14, -105.00732421875, 39.9939556939733, -104.9853515625, 40.01078714046552]
    [3413, 6203, 14, -105.00732421875, 39.977120098439634, -104.9853515625, 39.9939556939733]

The commands can be piped together to do this:

.. code-block:: console

    $ echo "[-104.99, 39.99, -105, 40]" \
    > | mercantile tiles - 14 \
    > | mercantile shapes - --indent 2 --precision 6
    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              [
                [
                  -105.007324,
                  39.993956
                ],
                [
                  -105.007324,
                  40.010787
                ],
                [
                  -104.985352,
                  40.010787
                ],
                [
                  -104.985352,
                  39.993956
                ],
                [
                  -105.007324,
                  39.993956
                ]
              ]
            ],
            "type": "Polygon"
          },
          "id": "(3413, 6202, 14)",
          "properties": {
            "title": "XYZ tile (3413, 6202, 14)"
          },
          "type": "Feature"
        },
        {
          "geometry": {
            "coordinates": [
              [
                [
                  -105.007324,
                  39.97712
                ],
                [
                  -105.007324,
                  39.993956
                ],
                [
                  -104.985352,
                  39.993956
                ],
                [
                  -104.985352,
                  39.97712
                ],
                [
                  -105.007324,
                  39.97712
                ]
              ]
            ],
            "type": "Polygon"
          },
          "id": "(3413, 6203, 14)",
          "properties": {
            "title": "XYZ tile (3413, 6203, 14)"
          },
          "type": "Feature"
        }
      ],
      "type": "FeatureCollection"
    }

If you have `geojsonio-cli <https://github.com/mapbox/geojsonio-cli>`__
installed, you can shoot this GeoJSON straight to `geojson.io
<http://geojson.io/>`__ for lightning-fast visualization and editing.

.. code-block:: console

    $ echo "[-104.99, 39.99, -105, 40]" \
    > | mercantile tiles - 14 \
    > | mercantile shapes - --compact \
    > | geojsonio

See Also
--------

`node-sphericalmercator <https://github.com/mapbox/node-sphericalmercator>`__
provides many of the same features for Node.
