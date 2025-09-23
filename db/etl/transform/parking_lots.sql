DROP TABLE IF EXISTS data.parking_lots;

CREATE TABLE data.parking_lots AS
SELECT 
    CAST(_id AS integer) AS id,
    NULLIF(last_geometry_maint, '')::text AS last_updated,
    geom AS geometry
FROM (
    SELECT 
        _id,
        last_geometry_maint,
        ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geom
    FROM staging.parking_lots_raw
) sub
WHERE geom IS NOT NULL
  AND ST_IsValid(geom)
  AND NOT ST_IsEmpty(geom);

ALTER TABLE data.parking_lots ADD PRIMARY KEY (id);

CREATE INDEX ON data.parking_lots USING GIST (geometry);