import json
import re

from db.db import execute_sql

def _detect_geom_col(row):
    for k, v in row.items():
        if isinstance(v, (dict, str)):
            try:
                obj = json.loads(v) if isinstance(v, str) else v
                if isinstance(obj,dict) and "type" in obj and "coordinates" in obj:
                    return k
            except Exception:
                pass
    return None

def parse_results(queries):
    layers = []

    for query in queries:
        print("[Parse] Executing: ", query)
        rows = execute_sql(query)
        colnames = list(rows[0].keys())
        #geom_col = "geometry"
        geom_col = _detect_geom_col(rows[0])
        prop_cols = [c for c in colnames if c != geom_col]

        features = []
        table_rows = []
        
        for row in rows:
            geom = None
            if geom_col and row.get(geom_col): 
                geom = json.loads(row[geom_col])
            #geom = json.loads(row[geom_col]) 
            props = {k: v for k,v in row.items() if k != geom_col}

            if geom:
                features.append({
                    "type": "Feature",
                    "geometry": geom,
                    "properties": props
                })
            table_rows.append([row.get(c) for c in prop_cols])
        
        match = re.search(r"\bfrom\s+([a-zA-Z0-9_\"\.]+)", query, re.IGNORECASE)
        if match:
            layer_name = match.group(1).replace('"', '')  # strip quotes if present
        else:
            layer_name = f"layer_{len(layers) + 1}"
        
        layers.append({
            "name": layer_name,
            "geojson": {
                "type": "FeatureCollection",
                "features": features
            },
            "columns": prop_cols,
            "rows": table_rows    
        })
    return layers 