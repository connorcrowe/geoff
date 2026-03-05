import math
from typing import Tuple

def _get_simplification_tolerance(z: int) -> float:
    if z <= 5:
        return 0.01      # Continent/country view - heavy simplification
    elif z <= 10:
        return 0.001     # Region/city view - moderate simplification
    elif z <= 14:
        return 0.0001    # Neighborhood view - light simplification
    else:
        return 0.000001   # Street level detail - minimal simplification


def build_mvt_query(base_query: str, layer_name: str, z: int, x: int, y: int) -> str:
    tolerance = _get_simplification_tolerance(z)
    
    # Build the MVT query using PostGIS ST_AsMVT
    # 1. Create tile bounds envelope
    # 2. Get base data (the original query)
    # 3. Filter to features intersecting tile + simplify geometry
    # 4. Convert to MVT format

    mvt_query = f"""
    WITH 
    tile_bounds AS (
        SELECT ST_TileEnvelope({z}, {x}, {y}) AS geometry
    ),
    base_data AS (
        {base_query[:-1]}
    ),
    tile_data AS (
        SELECT 
            base_data.id,
            ST_AsMVTGeom(
                ST_Transform(
                    ST_SimplifyPreserveTopology(base_data.geometry, {tolerance}),
                    3857  -- Web Mercator
                ),
                tile_bounds.geometry, -- ST_Transform(tile_bounds.geometry, 3857),
                4096,  -- extent (tile resolution)
                256,   -- buffer (pixels beyond tile edge)
                true   -- clip geometries to tile bounds
            ) AS geometry
        FROM base_data
        JOIN tile_bounds
        ON base_data.geometry && ST_Transform(tile_bounds.geometry, 4326) -- Tile is compared to spatial index of base_data here, which is 4326
    )
    SELECT ST_AsMVT(tile_data, '{layer_name}', 4096, 'geometry', 'id') AS mvt
    FROM tile_data
    WHERE geometry IS NOT NULL;
    """
    
    return mvt_query