
import json
from shapely import wkb

def convert(rows, colnames):
    # Identify geometry column (first that can be parsed as WKB)
    geom_index = None
    for i, name in enumerate(colnames):
        for r in rows:
            try:
                if r[i] is not None:
                    wkb.loads(r[i], hex=True)
                    geom_index = i
                    break
            except Exception: continue
        if geom_index is not None: break

    features = []
    table_rows = []
    for row in rows:
        props = {}
        geom = None

        for i, val in enumerate(row):
            if i == geom_index:
                try:
                    geom_obj = wkb.loads(val, hex=True) if val else None
                    geom = json.loads(json.dumps(geom_obj.__geo_interface__)) if geom_obj else None
                except Exception:
                    geom = None
            else:
                props[colnames[i]] = val

        if geom:
            features.append({
                "type": "Feature",
                "geometry": geom,
                "properties": props
            })

        table_rows.append([props.get(c) if c in props else row[colnames.index(c)] for c in colnames if colnames.index(c) != geom_index])

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    # Remove geometry column from table header
    table_columns = [c for i, c in enumerate(colnames) if i != geom_index]
    return geojson, table_columns, table_rows