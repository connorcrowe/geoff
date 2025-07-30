-- Create a staging table matching the CSV
DROP TABLE IF EXISTS neighbourhoods_raw;

CREATE TABLE neighbourhoods_raw (
    _id INTEGER,
    area_id INTEGER,
    area_attr_id INTEGER,
    parent_area_id INTEGER,
    area_short_code TEXT,
    area_long_code TEXT,
    area_name TEXT,
    area_desc TEXT,
    classification TEXT,
    classification_code TEXT,
    objectid INTEGER,
    geometry_text TEXT
);

-- Import CSV into staging table
COPY neighbourhoods_raw FROM '/import/neighbourhoods-4326.csv' WITH (
    FORMAT csv, 
    HEADER true, 
    QUOTE '"'
);

-- Convert GeoJSON text into real geometry and move into the real table
INSERT INTO neighbourhoods (
    _id, area_id, area_attr_id, parent_area_id, area_short_code,
    area_long_code, area_name, area_desc, classification,
    classification_code, objectid, geom
)
SELECT
    _id,
    area_id,
    area_attr_id,
    parent_area_id,
    area_short_code,
    area_long_code,
    area_name,
    area_desc,
    classification,
    classification_code,
    objectid,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry_text), 4326)
FROM neighbourhoods_raw;

-- Cleanup
DROP TABLE neighbourhoods_raw;