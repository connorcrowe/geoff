DROP TABLE IF EXISTS data.ambulance_stations;
CREATE TABLE data.ambulance_stations AS
SELECT
    CAST(_id AS integer) AS id,
    NULLIF(address_full, '')::text as address,
    NULLIF(municipality, '')::text as municipality,
    CAST(ems_id AS integer) AS ems_id,
    NULLIF(ems_name, '')::text as ems_name,
    NULLIF(ems_website, '')::text as ems_website,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.ambulance_stations_raw;

ALTER TABLE data.ambulance_stations ADD PRIMARY KEY (id);

CREATE INDEX ON data.ambulance_stations USING GIST (geometry);