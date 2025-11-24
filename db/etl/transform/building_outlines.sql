DROP TABLE IF EXISTS data.building_outlines;
CREATE TABLE data.building_outlines AS
SELECT
    -- CAST(_id AS integer) AS id,
    -- NULLIF(some_string, '')::text AS name,
    -- CAST(some_int AS integer) AS location_id,
    -- ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
    
    CAST(_id AS integer) AS id,
    NULLIF(subtype_desc, '')::text AS subtype_desc,
    CAST(subtype_code AS integer) AS subtype_code,
    CAST(elevation AS integer) AS elevation,
    CAST(derived_height AS integer) AS derived_height,
    CAST(objectid AS integer) AS objectid,
    NULLIF(last_attribute_maint, '')::text AS last_attribute_maint,
    NULLIF(last_geometry_maint, '')::text AS last_geometry_maint,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry

FROM staging.building_outlines_raw;

ALTER TABLE data.building_outlines ADD PRIMARY KEY (id);
CREATE INDEX ON data.building_outlines USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.building_outlines.id IS 'Unique identifier';
COMMENT ON COLUMN data.building_outlines.subtype_desc IS 'Text description of outline subtype ["Miscellaneous Structure", "Building Outline", "Garage"]';
COMMENT ON COLUMN data.building_outlines.subtype_code IS 'Short code categorizing outline subtype ';
COMMENT ON COLUMN data.building_outlines.elevation IS 'Ground elevation of the feature';
COMMENT ON COLUMN data.building_outlines.derived_height IS 'Height of the feature - Derived from LiDAR data';
COMMENT ON COLUMN data.building_outlines.objectid IS 'Unique ID of the feature';
COMMENT ON COLUMN data.building_outlines.last_attribute_maint IS 'Date of the last attribute edit';
COMMENT ON COLUMN data.building_outlines.last_geometry_maint IS 'Date of last geometry edit';
COMMENT ON COLUMN data.building_outlines.geometry IS 'Geometry: polygon location of the building';
