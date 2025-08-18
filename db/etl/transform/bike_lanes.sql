DROP TABLE IF EXISTS data.bike_lanes;
CREATE TABLE data.bike_lanes AS
SELECT
    CAST(_id AS integer) AS id,
    CAST(segment_id AS integer) AS segment_id,
    NULLIF(TRIM(installed::text), '')::integer AS installed_year,
    NULLIF(TRIM(upgraded::text), '')::integer AS upgraded_year,
    NULLIF(pre_amalgamation, '')::text AS pre_amalgamation,
    NULLIF(street_name, '')::text AS street_name,
    NULLIF(from_street, '')::text AS from_street,
    NULLIF(to_street, '')::text AS to_street,
    NULLIF(roadclass, '')::text AS roadclass,
    NULLIF(cnpclass, '')::text AS cnpclass,
    NULLIF(surface, '')::text AS surface,
    NULLIF(owner, '')::text AS owner,
    NULLIF(dir_loworder, '')::text AS dir_loworder,
    NULLIF(infra_loworder, '')::text AS infra_loworder,
    NULLIF(infra_highorder, '')::text AS lane_type,
    NULLIF(converted, '')::text AS converted,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.bike_lanes_raw;

ALTER TABLE data.bike_lanes ADD PRIMARY KEY (id);

CREATE INDEX ON data.bike_lanes USING GIST (geometry);