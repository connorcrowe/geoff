DROP TABLE IF EXISTS data.parks;
CREATE TABLE data.parks AS
SELECT
    CAST(_id AS integer) AS id,
    CAST(locationid AS integer) AS location_id,
    CAST(asset_id AS integer) AS asset_id,
    NULLIF(asset_name, '')::text AS name,
    NULLIF(type, '')::text AS type,
    NULLIF(amenities, '')::text AS amenities,
    NULLIF(address, '')::text AS address,
    NULLIF(phone, '')::text AS phone,
    NULLIF(url, '')::text AS url,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.parks_raw;

ALTER TABLE data.parks ADD PRIMARY KEY (id);

CREATE INDEX ON data.parks USING GIST (geometry);