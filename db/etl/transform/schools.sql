DROP TABLE IF EXISTS data.schools;
CREATE TABLE data.schools AS
SELECT
    CAST(_id AS integer) AS id,
    NULLIF(name, '')::text as name,
    NULLIF(school_type, '')::text as school_type,
    NULLIF(school_type_desc, '')::text as school_type_desc,
    NULLIF(board_name, '')::text as school_board_name,
    NULLIF(address_full, '')::text as address,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.schools_raw;

ALTER TABLE data.schools ADD PRIMARY KEY (id);

CREATE INDEX ON data.schools USING GIST (geometry);