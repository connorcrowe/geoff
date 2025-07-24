CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE bike_lanes (
    id SERIAL PRIMARY KEY,
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
    geom GEOMETRY(MULTILINESTRING, 4326)
);