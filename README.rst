==========
Mercantile
==========

.. image:: https://travis-ci.org/mapbox/mercantile.svg
   :target: https://travis-ci.org/mapbox/mercantile

.. image:: https://coveralls.io/repos/github/mapbox/mercantile/badge.svg?branch=master
   :target: https://coveralls.io/github/mapbox/mercantile?branch=master

Spherical mercator coordinate and tile utilities

The mercantile module provides ``ul(xtile, ytile, zoom)`` and ``bounds(xtile,
ytile, zoom)`` functions that respectively return the upper left corner and
bounding longitudes and latitudes for XYZ tiles, a ``xy(lng, lat)`` function
that returns spherical mercator x and y coordinates, a ``tile(lng, lat,
zoom)`` function that returns the tile containing a given point, and
quadkey conversion functions ``quadkey(xtile, ytile, zoom)`` and
``quadkey_to_tile(quadkey)`` for translating between quadkey and tile
coordinates.

.. code-block:: pycon

    >>> import mercantile
    >>> mercantile.ul(486, 332, 10)
    LngLat(lng=-9.140625, lat=53.33087298301705)
    >>> mercantile.bounds(486, 332, 10)
    LngLatBbox(west=-9.140625, south=53.12040528310657, east=-8.7890625, north=53.33087298301705)
    >>> mercantile.xy(*mercantile.ul(486, 332, 10))
    (-1017529.7205322663, 7044436.526761846)
    >>> mercantile.tile(*mercantile.ul(486, 332, 10) + (10,))
    Tile(x=486, y=332, z=10)
    >>> mercantile.quadkey(486, 332, 10)
    '0313102310'
    >>> mercantile.quadkey_to_tile('0313102310')
    Tile(x=486, y=332, z=10)

Also in mercantile are functions to traverse the tile stack.

.. code-block:: pycon

    >>> mercantile.parent(486, 332, 10)
    Tile(x=243, y=166, z=9)
    >>> mercantile.children(mercantile.parent(486, 332, 10))
    [Tile(x=486, y=332, z=10), Tile(x=487, y=332, z=10), Tile(x=487, y=333, z=10), Tile(x=486, y=333, z=10)]

Named tuples are used to represent tiles, coordinates, and bounding boxes.

Mercantile CLI
==============

Mercantile's command line interface, named "mercantile", has commands for 
getting the shapes of Web Mercator tiles as GeoJSON and getting the tiles
that intersect with a GeoJSON bounding box. 

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
      quadkey   Convert to/from quadkeys.
      shapes    Write the shapes of tiles as GeoJSON.
      tiles     List tiles that overlap or contain a lng/lat point, bounding box,
                or GeoJSON objects.

See `docs/cli.rst <docs/cli.rst>`__ for more about the mercantile program.


See Also
========

`node-sphericalmercator <https://github.com/mapbox/node-sphericalmercator>`__
provides many of the same features for Node.

`tilebelt <https://github.com/mapbox/tilebelt>`__ has some of the GeoJSON
features as mercantile and a few more (tile parents, quadkey).
