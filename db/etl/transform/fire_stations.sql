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