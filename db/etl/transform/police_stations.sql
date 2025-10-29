DROP TABLE IF EXISTS data.police_stations;
CREATE TABLE data.police_stations AS
SELECT
    CAST(_id AS integer) AS id,
    NULLIF(facility, '')::text as name,
    NULLIF(address, '')::text as address,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.police_stations_raw;

ALTER TABLE data.police_stations ADD PRIMARY KEY (id);
CREATE INDEX ON data.police_stations USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.police_stations.id IS 'Unique identifier';
COMMENT ON COLUMN data.police_stations.name IS 'Name of the station';
COMMENT ON COLUMN data.police_stations.address IS 'Street address pf tje station';
COMMENT ON COLUMN data.police_stations.geometry IS 'Geometry: point location of the station';