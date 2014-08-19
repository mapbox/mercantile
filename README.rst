mercantile
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
--------------

Mercantile's command line interface, named "mercantile", has commands for 
getting the shapes of Web Mercator tiles as GeoJSON and getting the tiles
that intersect with a GeoJSON bounding box. They can be combined like this:

.. code-block:: console

    $ echo "[-104.99, 39.99, -105, 40]" \
    > | mercantile tiles - 14 \
    > | mercantile shapes -
    {"features": [{"geometry": {"coordinates": [[[-105.00732421875, 39.9939556939733], [-105.00732421875, 40.01078714046552], [-104.9853515625, 40.01078714046552], [-104.9853515625, 39.9939556939733], [-105.00732421875, 39.9939556939733]]], "type": "Polygon"}, "id": "(3413, 6202, 14)", "properties": {"title": "XYZ tile (3413, 6202, 14)"}, "type": "Feature"}, {"geometry": {"coordinates": [[[-105.00732421875, 39.977120098439634], [-105.00732421875, 39.9939556939733], [-104.9853515625, 39.9939556939733], [-104.9853515625, 39.977120098439634], [-105.00732421875, 39.977120098439634]]], "type": "Polygon"}, "id": "(3413, 6203, 14)", "properties": {"title": "XYZ tile (3413, 6203, 14)"}, "type": "Feature"}], "type": "FeatureCollection"}

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
