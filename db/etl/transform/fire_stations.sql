DROP TABLE IF EXISTS data.fire_stations;
CREATE TABLE data.fire_stations AS
SELECT
    CAST(_id AS integer) AS id,
    NULLIF(address, '')::text as address,
    NULLIF(municipality_name, '')::text as municipality,
    CAST(station AS integer) AS station_no,
    CAST(year_build AS integer) as year_built,
    NULLIF(type_desc, '')::text as type,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.fire_stations_raw;

ALTER TABLE data.fire_stations ADD PRIMARY KEY (id);
CREATE INDEX ON data.fire_stations USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.fire_stations.id IS 'Unique identifier';
COMMENT ON COLUMN data.fire_stations.address IS 'Street address of fire stations';
COMMENT ON COLUMN data.fire_stations.municipality IS 'Municipality of the station';
COMMENT ON COLUMN data.fire_stations.station_no IS 'FD number of the station';
COMMENT ON COLUMN data.fire_stations.year_built IS 'Year the station was built';
COMMENT ON COLUMN data.fire_stations.type IS 'Fire station or operaitons centre';
COMMENT ON COLUMN data.fire_stations.geometry IS 'Geometry: point location of the fire station';