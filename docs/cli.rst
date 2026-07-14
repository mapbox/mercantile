Command line interface
======================

.. code-block:: console

	$ mercantile --help
	Usage: mercantile [OPTIONS] COMMAND [ARGS]...

	  Command line interface for the Mercantile Python package.

	Options:
	  -v, --verbose  Increase verbosity.
	  -q, --quiet    Decrease verbosity.
	  --version      Show the version and exit.
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
performs the reverse operation.

.. code-block:: console

    $ mercantile shapes "[2331, 1185, 12]" | mercantile tiles 12
    [2331, 1185, 12]

If you have `geojsonio-cli <https://github.com/mapbox/geojsonio-cli>`_
installed, you can shoot this GeoJSON straight to `geojson.io
<http://geojson.io/>`__ for lightning-fast visualization and editing.

.. code-block:: console

    $ echo "[-105, 39.99, -104.99, 40]" \
    | mercantile tiles 14 \
    | mercantile shapes --collect \
    | geojsonio

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

bounding-tile
-------------

The bounding-tile command writes the input's bounding tile, the smallest
mercator tile of any resolution that completely contains the input.

.. code-block:: console

	$ mercantile bounding-tile --help
	Usage: mercantile bounding-tile [OPTIONS] [INPUT]

	  Print the Web Mercator tile at ZOOM level bounding GeoJSON [west, south,
	  east, north] bounding boxes, features, or collections read from stdin.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Example:

	  echo "[-105.05, 39.95, -105, 40]" | mercantile bounding-tile
	  [426, 775, 11]

	Options:
	  --seq / --lf  Write a RS-delimited JSON sequence (default is LF).
	  --help        Show this message and exit.

Note that when the input crosses longitude 0 or latitude 0, or any such tile
boundary, the bounding tile will be at a shallow zoom level.

.. code-block:: console

    $ echo "[-1, 1, 1, 2]" | mercantile bounding-tile
    [0, 0, 0]
    $ echo "[-91, 1, -89, 2]" | mercantile bounding-tile
    [0, 0, 1]

Compare these bounding tiles to the one for a similarly size input box shifted
away from the zoom=1 tile intersection.

.. code-block:: console

    $ echo "[-92, 1, -91, 2]" | mercantile bounding-tile
    [31, 63, 7]

children
--------

.. code-block:: console

	$ mercantile children --help
	Usage: mercantile children [OPTIONS] [INPUT]

	  Takes [x, y, z] tiles as input and writes children to stdout in the same
	  form.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Example:

	  echo "[486, 332, 10]" | mercantile children
	  [972, 664, 11]
	  [973, 664, 11]
	  [973, 665, 11]
	  [972, 665, 11]

	Options:
	  --depth INTEGER  Number of zoom levels to traverse (default is 1).
	  --help           Show this message and exit.

neighbors
---------

The neighbors command writes out the tiles adjacent to the input tile.

.. code-block:: console

	$ mercantile neighbors --help
	Usage: mercantile neighbors [OPTIONS] [INPUT]

	  Takes [x, y, z] tiles as input and writes adjacent tiles on the same zoom
	  level to stdout in the same form.

	  There are no ordering guarantees for the output tiles.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Example:

	  echo "[486, 332, 10]" | mercantile neighbors
	  [485, 331, 10]
	  [485, 332, 10]
	  [485, 333, 10]
	  [486, 331, 10]
	  [486, 333, 10]
	  [487, 331, 10]
	  [487, 332, 10]
	  [487, 333, 10]

	Options:
	  --help  Show this message and exit.

parent
------

The parent command writes out the tiles that contain the input tiles.

.. code-block:: console

	$ mercantile parent --help
	Usage: mercantile parent [OPTIONS] [INPUT]

	  Takes [x, y, z] tiles as input and writes parents to stdout in the same
	  form.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Example:

	  echo "[486, 332, 10]" | mercantile parent
	  [243, 166, 9]

	Options:
	  --depth INTEGER  Number of zoom levels to traverse (default is 1).
	  --help           Show this message and exit.

quadkey
-------

The quadkey command converts between [x, y, z] arrays and quadkey strings.

.. code-block:: console

	$ mercantile parent --help
	Usage: mercantile quadkey [OPTIONS] [INPUT]

	  Takes [x, y, z] tiles or quadkeys as input and writes quadkeys or a [x, y,
	  z] tiles to stdout, respectively.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Examples:

	  echo "[486, 332, 10]" | mercantile quadkey
	  0313102310

	  echo "0313102310" | mercantile quadkey
	  [486, 332, 10]

	Options:
	  --help  Show this message and exit.

shapes
------

The shapes command writes tile shapes to several forms of GeoJSON.

.. code-block:: console

	$ mercantile shapes --help
	Usage: mercantile shapes [OPTIONS] [INPUT]

	  Print tiles as GeoJSON feature collections or sequences.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Tile descriptions may be either an [x, y, z] array or a JSON object of the
	  form

		{"tile": [x, y, z], "properties": {"name": "foo", ...}}

	  In the latter case, the properties object will be used to update the
	  properties object of the output feature.

		  Example:

			  echo "[486, 332, 10]" | mercantile shapes --precision 4 --bbox
			  [-9.1406, 53.1204, -8.7891, 53.3309]

	Options:
	  --precision INTEGER       Decimal precision of coordinates.
	  --indent INTEGER          Indentation level for JSON output
	  --compact / --no-compact  Use compact separators (',', ':').
	  --geographic              Output in geographic coordinates (the default).
	  --mercator                Output in Web Mercator coordinates.
	  --seq                     Write a RS-delimited JSON sequence (default is
								LF).

	  --feature                 Output as sequence of GeoJSON features (the
								default).

	  --bbox                    Output as sequence of GeoJSON bbox arrays.
	  --collect                 Output as a GeoJSON feature collections.
	  --extents / --no-extents  Write shape extents as ws-separated strings
								(default is False).

	  --buffer FLOAT            Shift shape x and y values by a constant number
	  --help                    Show this message and exit.

tiles
-----

With the tiles command you can write descriptions of tiles intersecting with
a geographic point, bounding box, or GeoJSON object.

.. code-block:: console

	$ mercantile tiles --help
	Usage: mercantile tiles [OPTIONS] [ZOOM] [INPUT]

	  Lists Web Mercator tiles at ZOOM level intersecting GeoJSON [west, south,
	  east, north] bounding boxen, features, or collections read from stdin.
	  Output is a JSON [x, y, z] array.

	  Input may be a compact newline-delimited sequences of JSON or a pretty-
	  printed ASCII RS-delimited sequence of JSON (like
	  https://tools.ietf.org/html/rfc8142 and
	  https://tools.ietf.org/html/rfc7159).

	  Example:

	  $ echo "[-105.05, 39.95, -105, 40]" | mercantile tiles 12
	  [852, 1550, 12]
	  [852, 1551, 12]
	  [853, 1550, 12]
	  [853, 1551, 12]

	Options:
	  --seq / --lf  Write a RS-delimited JSON sequence (default is LF).
	  --help        Show this message and exit.

		$ echo "[-105, 39.99, -104.99, 40]" | mercantile tiles 14
		[3413, 6202, 14]
		[3413, 6203, 14]


When supplying GeoJSON as input, you may need to first compact with the help of ``jq``

.. code-block:: console

    $ cat input.geojson | jq -c . | mercantile tiles 14
