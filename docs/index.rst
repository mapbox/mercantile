.. Mercantile documentation master file, created by
   sphinx-quickstart on Tue Nov 14 23:21:41 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Mercantile's documentation!
======================================

Mercantile is a module of utilities for working with XYZ style spherical
mercator tiles (as in Google Maps, OSM, Mapbox, etc.) and includes a set of
command line programs built on these utilities.


Quick start
-----------

In the XYZ tiling system, the region of the world from 85.0511 (more precisely:
``arctan(sinh(π))``) degrees south of the Equator to 85.0511 degrees north is
covered at zoom level 0 by a single tile. The number of tiles at each zoom
level is ``2**(2*Z)``. At zoom level 1, we have 4 tiles.

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


You can get the tile containing a longitude and latitude pair from the ``mercantile.tile``
function.

.. code-block:: pycon

    >>> import mercantile
    >>> mercantile.tile(-105.0, 40.0, 1)
    Tile(x=0, y=0, z=1)

You can get the geographic (longitude and latitude) bounds of a tile from the
``mercantile.bounds`` function.

.. code-block:: pycon

    >>> mercantile.bounds(mercantile.Tile(x=0, y=0, z=1))
    LngLatBbox(west=-180.0, south=0.0, east=0.0, north=85.0511287798066)


API reference
-------------

.. automodule:: mercantile
   :members:
   :undoc-members:
   :show-inheritance:


CLI guide
---------

.. toctree::
   :maxdepth: 2

   cli


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

