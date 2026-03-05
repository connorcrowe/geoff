import json
import re

from db.db import execute_sql
from services import layer_store
from core import mvt_builder


def _detect_geom_col(row):
    for k, v in row.items():
        # Check for 'geometry' column name
        if k.lower() == 'geometry':
            return k

    return None


def parse_results(queries):
    layers = []

    for query in queries:
        print("[Parse] Executing: ", query)
        rows = execute_sql(query)
        
        if not rows:
            continue
        
        colnames = list(rows[0].keys())
        geom_col = _detect_geom_col(rows[0])
        
        # Exclude geometry from attribute columns
        prop_cols = [c for c in colnames if c != geom_col]
        
        # Build table rows (attributes only, no geometry)
        table_rows = []
        for row in rows:
            table_rows.append([row.get(c) for c in prop_cols])
        
        # Extract layer name from query
        match = re.search(r"\bfrom\s+([a-zA-Z0-9_\"\.]+)", query, re.IGNORECASE)
        if match:
            layer_name = match.group(1).replace('"', '')
        else:
            layer_name = f"layer_{len(layers) + 1}"
        
        # Store the query for MVT tile generation
        layer_id = layer_store.create_layer(query, layer_name)
        
        layers.append({
            "name": layer_name,
            "layer_id": layer_id,
            "tile_url": f"/api/tiles/{layer_id}/{{z}}/{{x}}/{{y}}.pbf",
            "columns": prop_cols,
            "rows": table_rows
        })
    
    return layers