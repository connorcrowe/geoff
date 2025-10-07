
import json
from shapely import wkb

def convert_to_geo_layers(rows, colnames):
    """Convert SQL rows with 1 or more geometry columns into distinct layers."""
    geom_indices = _find_geometry_columns(rows, colnames)
    print(f"[GEO] Indicies: {geom_indices}")
    layers = []

    for geom_index in geom_indices:
        layer = _build_layer(rows, colnames, geom_index)
        layers.append(layer)

    return layers

def _find_geometry_columns(rows, colnames):
    """Identify all geometry columns in a set of data"""
    geom_indices = []

    for i, name in enumerate(colnames):
        for r in rows:
            try:
                if r[i] is not None:
                    wkb.loads(r[i], hex=True)
                    geom_indices.append(i)
                    break
            except Exception: continue
    return geom_indices

def _build_layer(rows, colnames, geom_index):
    """Build one layer (GeoJSON + table) from a specific geo column index"""
    print(f"[GEO] Buidling index: {geom_index}")
    features = []
    table_rows = []

    for row in rows:
        props = {}
        geom = None

        for i, val in enumerate(row):
            if i == geom_index:
                geom = _convert_wkb_to_geojson(val)
            else: 
                props[colnames[i]] = val
        
        if geom:
            features.append({
                "type": "Feature",
                "geometry": geom,
                "properties": props
            })
        
        # Keep only non-geometry values
        table_rows.append([props.get(c) for c in colnames if colnames.index(c) != geom_index])
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    layer_name = colnames[geom_index]# or f"layer_{geom_index}"
    table_columns = [c for i, c in enumerate(colnames) if i != geom_index]

    print(f"[GEO] Returning {table_columns}")
    return {
        "name": layer_name,
        "geojson": geojson,
        "columns": table_columns,
        "rows": table_rows
    }

def _convert_wkb_to_geojson(val):
    """Convert geometry column from WKB to geojson"""
    try:
        geom_obj = wkb.loads(val, hex=True) if val else None
        geom = json.loads(json.dumps(geom_obj.__geo_interface__)) if geom_obj else None
    except Exception as e:
        geom = None
        print(e)
    return geom