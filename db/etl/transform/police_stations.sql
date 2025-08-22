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