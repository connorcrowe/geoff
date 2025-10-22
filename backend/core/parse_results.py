import json
import re

from db.db import execute_sql


def parse_results(queries):
    layers = []

    for query in queries:
        print("AAA. Executing: ", query)
        rows = execute_sql(query)

        colnames = list(rows[0].keys())
        geom_col = "geometry"
        prop_cols = [c for c in colnames if c != geom_col]

        features = []
        table_rows = []
        
        for row in rows:
            geom = json.loads(row[geom_col])
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