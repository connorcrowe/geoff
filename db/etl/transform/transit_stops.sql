DROP TABLE IF EXISTS data.transit_stops;
CREATE TABLE data.transit_stops AS
SELECT
    --CAST(_id AS integer) AS id,
    --NULLIF(some_string, '')::text AS name,
    --CAST(some_int AS integer) AS location_id,
    --ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry

    CAST(stop_id AS integer) AS id,
    NULLIF(stop_name, '')::text AS name,
    CAST(stop_desc AS integer) AS description,
    CAST(wheelchair_boarding AS integer) AS wheelchair_boarding,
    CAST(location_type AS integer) AS location_type,
    ST_SetSRID(ST_Point(stop_lon, stop_lat), 4326) AS geometry
FROM staging.gtfs_stops;

ALTER TABLE data.transit_stops ADD PRIMARY KEY (id);
CREATE INDEX ON data.transit_stops USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.transit_stops.id IS 'Unique identifier';
COMMENT ON COLUMN data.transit_stops.name IS 'Name of the transit stop';
COMMENT ON COLUMN data.transit_stops.description IS 'Description of the stop';
COMMENT ON COLUMN data.transit_stops.wheelchair_boarding IS 'Whether there is accessible boarding at the stop';
COMMENT ON COLUMN data.transit_stops.location_type IS 'Location type of the stop';
COMMENT ON COLUMN data.transit_stops.geometry IS 'Geometry: point location of the stop';
