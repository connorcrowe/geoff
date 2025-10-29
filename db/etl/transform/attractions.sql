DROP TABLE IF EXISTS data.attractions;
CREATE TABLE data.attractions AS
SELECT
    --CAST(_id AS integer) AS id,
    --NULLIF(some_string, '')::text AS name,
    --CAST(some_int AS integer) AS location_id,
    --ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry

    CAST(_id AS integer) AS id,
    NULLIF(name, '')::text AS name,
    NULLIF(category, '')::text AS category,
    NULLIF(phone, '')::text AS phone,
    NULLIF(website, '')::text AS website,
    NULLIF(address_full, '')::text AS address,
    NULLIF(municipality, '')::text AS municipality,
    CAST(centreline AS integer) AS centreline,
    NULLIF(ward, '')::text AS ward,
    CAST(ward_2021 AS integer) AS ward_id,
    NULLIF(attraction, '')::text AS description,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326) AS geometry
FROM staging.attractions_raw;

ALTER TABLE data.attractions ADD PRIMARY KEY (id);
CREATE INDEX ON data.attractions USING GIST (geometry);

-- Add descriptions
COMMENT ON COLUMN data.attractions.id IS 'Unique identifier';
COMMENT ON COLUMN data.attractions.name IS 'Name of the attraction or point of interest';
COMMENT ON COLUMN data.attractions.category IS 'Category or type that the attraction is';
COMMENT ON COLUMN data.attractions.phone IS 'Business phone number if available';
COMMENT ON COLUMN data.attractions.website IS 'Business website if available';
COMMENT ON COLUMN data.attractions.address IS 'Street address of attraction';
COMMENT ON COLUMN data.attractions.municipality IS 'Municipality of the attraction';
COMMENT ON COLUMN data.attractions.centreline IS 'ID key for Centreline table';
COMMENT ON COLUMN data.attractions.ward IS 'Name of Ward attraction is in';
COMMENT ON COLUMN data.attractions.ward_id IS 'ID of Ward attraction is in';
COMMENT ON COLUMN data.attractions.description IS 'Description of the attraction or point of interest';
COMMENT ON COLUMN data.attractions.geometry IS 'Geometry: point location of the attraction';
