DROP TABLE IF EXISTS data.wards;
CREATE TABLE data.wards AS
SELECT
    --CAST(_id AS integer) AS id,
    --NULLIF(some_string, '')::text AS name,
    --CAST(some_int AS integer) AS location_id,
    --ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry

    CAST(_id AS integer) AS id,
    NULLIF(area_name, '')::text AS name,
    CAST(area_short_code AS integer) AS ward_id,
    --CAST(area_id AS integer) AS area_id,
    --CAST(area_type_id AS integer) AS area_type_id,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.wards_raw;

ALTER TABLE data.wards ADD PRIMARY KEY (id);
CREATE INDEX ON data.wards USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.wards.id IS 'Unique identifier';
COMMENT ON COLUMN data.wards.name IS 'Name of the ward';
COMMENT ON COLUMN data.wards.ward_id IS 'Ward ID for linking to other tables';
COMMENT ON COLUMN data.wards.geometry IS 'Geometry: polygon boundary of the ward';
