Quick start
===========

In the XYZ tiling system, the region of the world from 85.0511 (more precisely:
``arctan(sinh(π))``) degrees south of the Equator to 85.0511 degrees north is
covered at zoom level 0 by a single tile. The number of tiles at each zoom
level is ``4 ** Z``. At zoom level 1, we have 4 tiles.

.. code-block:: none


                    +-------------+-------------+  85.0511 deg N
                    |             |             |
                    |    x: 0     |    x: 1     |
                    |    y: 0     |    y: 0     |
                    |    z: 1     |    z: 1     |
                    |             |             |
                    +-------------+-------------+   0.0 deg N
                    |             |             |
                    |    x: 0     |    x: 1     |
                    |    y: 1     |    y: 1     |
                    |    z: 1     |    z: 1     |
                    |             |             |
                    +-------------+-------------+  85.0511 deg S

                180.0 deg W               180.0 deg E


You can get the tile containing a longitude and latitude pair from the
``mercantile.tile`` function.

.. code-block:: pycon

    >>> import mercantile
    >>> mercantile.tile(-105.0, 40.0, 1)
    Tile(x=0, y=0, z=1)

You can get the geographic (longitude and latitude) bounds of a tile from the
``mercantile.bounds`` function.

.. code-block:: pycon

    >>> mercantile.bounds(mercantile.Tile(x=0, y=0, z=1))
    LngLatBbox(west=-180.0, south=0.0, east=0.0, north=85.0511287798066)
