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

