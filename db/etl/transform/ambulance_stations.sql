DROP TABLE IF EXISTS data.ambulance_stations;
CREATE TABLE data.ambulance_stations AS
SELECT
    CAST(_id AS integer) AS id,
    NULLIF(address_full, '')::text as address,
    NULLIF(municipality, '')::text as municipality,
    CAST(ems_id AS integer) AS ems_id,
    NULLIF(place_name, '')::text as name,
    NULLIF(ems_name, '')::text as ems_name,
    NULLIF(ems_website, '')::text as ems_website,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.ambulance_stations_raw;

ALTER TABLE data.ambulance_stations ADD PRIMARY KEY (id);
CREATE INDEX ON data.ambulance_stations USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.ambulance_stations.id IS 'Unique identifier';
COMMENT ON COLUMN data.ambulance_stations.address IS 'Street address of the station';
COMMENT ON COLUMN data.ambulance_stations.municipality IS 'Municipality of the station';
COMMENT ON COLUMN data.ambulance_stations.name IS 'Name of the station';
COMMENT ON COLUMN data.ambulance_stations.ems_id IS 'EMS ID';
COMMENT ON COLUMN data.ambulance_stations.ems_name IS 'EMS short name of the station';
COMMENT ON COLUMN data.ambulance_stations.ems_website IS 'Website of ambulance station';
COMMENT ON COLUMN data.ambulance_stations.geometry IS 'Geometry: point location of the station';