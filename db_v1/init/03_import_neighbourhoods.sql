-- Create a staging table matching the CSV
DROP TABLE IF EXISTS neighbourhoods_raw;

CREATE TABLE neighbourhoods_raw (
    id INTEGER,
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
    geometry TEXT
);

-- Import CSV into staging table
COPY neighbourhoods_raw FROM '/import/neighbourhoods-4326.csv' WITH (
    FORMAT csv, 
    HEADER true,
    QUOTE '"'
);

-- Convert GeoJSON text into real geometry and move into the real table
INSERT INTO neighbourhoods (
    id, area_id, area_attr_id, parent_area_id, area_short_code,
    area_long_code, area_name, area_desc, classification,
    classification_code, objectid, geometry
)
SELECT
    id,
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
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326)
FROM neighbourhoods_raw;

-- Add spatial index for neighbourhood polygons
CREATE INDEX idx_neighbourhoods_geometry ON neighbourhoods USING GIST (geometry);

-- Cleanup
DROP TABLE neighbourhoods_raw;