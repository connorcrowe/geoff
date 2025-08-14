DROP TABLE IF EXISTS data.neighbourhoods;
CREATE TABLE data.neighbourhoods AS
SELECT 
    CAST(_id AS integer) AS id,
    CAST(area_id AS bigint) AS area_id,
    CAST(area_attr_id AS bigint) AS area_attr_id,
    NULLIF(TRIM(area_short_code::text), '')::integer AS area_short_code,
    NULLIF(TRIM(area_long_code::text), '')::integer AS area_long_code,
    NULLIF(area_name, '')::text AS area_name,
    NULLIF(area_desc, '')::text AS area_desc,
    NULLIF(classification, '')::text AS classification,
    NULLIF(classification_code, '')::text AS classification_code,
    CAST(objectid AS bigint) AS objectid,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.neighbourhoods_raw;

ALTER TABLE data.neighbourhoods ADD PRIMARY KEY (id);

CREATE INDEX ON data.neighbourhoods USING GIST (geometry);