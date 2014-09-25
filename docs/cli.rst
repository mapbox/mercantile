Command line interface
======================

.. code-block:: console

    $ mercantile
    Usage: mercantile [OPTIONS] COMMAND [ARGS]...

      Command line interface for the Mercantile Python package.

    Options:
      -v, --verbose  Increase verbosity.
      -q, --quiet    Decrease verbosity.
      --help         Show this message and exit.

    Commands:
      children  Write the children of the tile.
      parent    Write the parent tile.
      shapes    Write the shapes of tiles as GeoJSON.
      tiles     List tiles overlapped or contained by a lng/lat bounding box.

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
