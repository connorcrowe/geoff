-- Create staging table
DROP TABLE IF EXISTS parks_raw;

CREATE TABLE parks_raw (
    _id INT,
    location_id INT,
    asset_id INT,
    asset_name TEXT,
    type TEXT,
    amenities TEXT,
    address TEXT,
    phone TEXT,
    url TEXT,
    geometry JSONB
);

-- Import CSV 
COPY parks_raw FROM '/import/parks-and-recreation-facilities-4326.csv' WITH (
    FORMAT csv,
    HEADER
);

-- Insert cleaned and parsed data
INSERT INTO parks (
    location_id,
    asset_id,
    name,
    type,
    amenities,
    address,
    phone,
    url,
    geometry
)
SELECT
    location_id,
    asset_id,
    asset_name,
    type,
    amenities,
    address,
    phone,
    url,
    ST_SetSRID(
        ST_MakePoint(
            (geometry->'coordinates'->0->0)::TEXT::FLOAT,
            (geometry->'coordinates'->0->1)::TEXT::FLOAT
        ),
        4326
    ) AS geometry
FROM parks_raw;

-- Index for spatial queries
CREATE INDEX idx_parks_geometry ON parks USING GIST (geometry);

-- Cleanup
DROP TABLE parks_raw;