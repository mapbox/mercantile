Command line interface
======================

.. code-block:: console

    $ mercantile --help
    Usage: mercantile [OPTIONS] COMMAND [ARGS]...

      Command line interface for the Mercantile Python package.

    Options:
      -v, --verbose  Increase verbosity.
      -q, --quiet    Decrease verbosity.
      --help         Show this message and exit.

    Commands:
      bounding-tile  Print the bounding tile of a lng/lat point, bounding box, or
                     GeoJSON objects.
      children       Print the children of the tile.
      neighbors      Print the neighbors of the tile.
      parent         Print the parent tile.
      quadkey        Convert to/from quadkeys.
      shapes         Print the shapes of tiles as GeoJSON.
      tiles          Print tiles that overlap or contain a lng/lat point, bounding
                     box, or GeoJSON objects.

Examples
--------

``mercantile shapes`` generates GeoJSON from tiles and ``mercantile tiles``
does the reverse operation.

.. code-block:: console

    $ mercantile shapes "[2331, 1185, 12]" | mercantile tiles 12
    [2331, 1185, 12]

``mercantile parent`` and ``mercantile children`` traverse the hierarchy
of Web Mercator tiles.

.. code-block:: console

    $ mercantile parent "[2331,1185,12]" | mercantile children
    [2330, 1184, 12]
    [2331, 1184, 12]
    [2331, 1185, 12]
    [2330, 1185, 12]

``mercantile quadkey`` will convert to/from quadkey representations of tiles.

.. code-block:: console

   $ mercantile quadkey "[486, 332, 10]"
   0313102310

   $ mercantile quadkey 0313102310
   [486, 332, 10]

shapes
------

The shapes command writes Mercator tile shapes to several forms of GeoJSON.

.. code-block:: console

    $ echo "[106, 193, 9]" | mercantile shapes --indent 2 --precision 6
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

bounding-tile
-------------

With the bounding-tile command you can write the input's bounding tile, the
smallest mercator tile of any resolution that completely contains the input.

.. code-block:: console

    $ echo "[-105, 39.99, -104.99, 40]" | mercantile bounding-tile
    [1706, 3101, 13]

Note well that when the input crosses lng 0 or lat 0, or any such tile 
boundary, the bounding tile will be at a shallow zoom level.

.. code-block:: console

    $ echo "[-1, 1, 1, 2]" | mercantile bounding-tile
    [0, 0, 0]
    $ echo "[-91, 1, -89, 2]" | mercantile bounding-tile
    [0, 0, 1]

Compare these bounding tiles to the one for a similarly size input box
shifted away from the zoom=1 tile intersection.

.. code-block:: console

    $ echo "[-92, 1, -91, 2]" | mercantile tiles bounding-tile
    [31, 63, 7]

tiles
-----

With the tiles command you can write descriptions of tiles intersecting with
a geographic point, bounding box, or GeoJSON object.

.. code-block:: console

    $ echo "[-105, 39.99, -104.99, 40]" | mercantile tiles 14
    [3413, 6202, 14]
    [3413, 6203, 14]


The commands can be piped together to do this:

.. code-block:: console

    $ echo "[-105, 39.99, -104.99, 40]" \
    > | mercantile tiles 14 \
    > | mercantile shapes --indent 2 --precision 6
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

or do a round trip like this

.. code-block:: console

    $  echo "[106, 193, 9]" | mercantile shapes | mercantile tiles 9
    [106, 193, 9]

If you have `geojsonio-cli <https://github.com/mapbox/geojsonio-cli>`_ installed, you can shoot this GeoJSON straight to `geojson.io <http://geojson.io/>`__ for lightning-fast visualization and editing.

.. code-block:: console

    $ echo "[-105, 39.99, -104.99, 40]" \
    | mercantile tiles 14 \
    | mercantile shapes --collect \
    | geojsonio

When supplying GeoJSON as input, you may need to first compact with the help of ``jq``

.. code-block:: console

    $ cat input.geojson | jq -c . | mercantile tiles 14
