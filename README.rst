mercantile
==========

Spherical mercator coordinate and tile utilities

The mercantile module provides ``ul(xtile, ytile, zoom)`` and ``bbox(xtile,
ytile, zoom)`` functions that return longitudes and latitudes for XYZ tiles,
and a ``xy(lon, lat)`` function that returns spherical mercator x and
y coordinates.

.. code-block:: pycon

    >>> import mercantile
    >>> mercantile.ul(486, 332, 10)
    (-9.140625, 53.33087298301705)
    >>> mercantile.bbox(486, 332, 10)
    (-9.140625, 53.12040528310657, -8.7890625, 53.33087298301705)
    >>> mercantile.xy(*mercantile.ul(486, 332, 10))
    (-1017529.7205322663, 7044436.526761846)

mercantile.tool
---------------

Mercantile includes a script that writes the extent of an XYZ tile out as
GeoJSON.

.. code-block:: console

    $ python -mmercantile.tool 20,35,6
    {"type": "FeatureCollection", "features": [{"geometry": {"type": "Polygon", "coordinates": [[[-67.5, -21.943045533438177], [-67.5, -16.636191878397653], [-61.875, -16.636191878397653], [-61.875, -21.943045533438177], [-67.5, -21.943045533438177]]]}, "type": "Feature", "id": "20,35,6", "properties": {"title": "XYZ tile 20,35,6"}}]}

If you have `geojsonio-cli <https://github.com/mapbox/geojsonio-cli>`__
installed, you can shoot this GeoJSON straight to `geojson.io
<http://geojson.io/>`__ for lightning-fast visualization and editing.

.. code-block:: console

    $ python -mmercantile.tool 20,35,6 | geojsonio

