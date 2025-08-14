-- Create a staging table
DROP TABLE IF EXISTS bike_lanes_raw;

CREATE TABLE bike_lanes_raw (
    id INTEGER,
    segment_id INTEGER,
    installed INTEGER,
    upgraded INTEGER,
    pre_amalgamation TEXT,
    street_name TEXT,
    from_street TEXT,
    to_street TEXT,
    roadclass TEXT,
    cnpclass TEXT,
    surface TEXT,
    owner TEXT,
    dir_loworder TEXT,
    infra_loworder TEXT,
    infra_highorder TEXT,
    converted INTEGER,
    geometry TEXT  -- GeoJSON as string
);

-- Import CSV 
COPY bike_lanes_raw FROM '/import/cleaned-bike-lanes.csv' WITH (
    FORMAT csv,
    HEADER,
    NULL ''
);

-- Convert GeoJSON text into real geometry and move into the real table
INSERT INTO bike_lanes (
    segment_id, installed, upgraded, pre_amalgamation, street_name,
    from_street, to_street, roadclass, cnpclass, surface, owner,
    dir_loworder, infra_loworder, infra_highorder, converted, geometry
)
SELECT
    segment_id, installed, upgraded, pre_amalgamation, street_name,
    from_street, to_street, roadclass, cnpclass, surface, owner,
    dir_loworder, infra_loworder, infra_highorder, converted,
    ST_SetSRID(ST_GeomFromGeoJSON(geometry), 4326)
FROM bike_lanes_raw;

-- Add spatial index for performance on spatial queries
CREATE INDEX idx_bike_lanes_geometry ON bike_lanes USING GIST (geometry);

-- Cleanup
DROP TABLE bike_lanes_raw;