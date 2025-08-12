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
    geometry GEOMETRY(MULTILINESTRING, 4326)
);

CREATE TABLE neighbourhoods (
    id SERIAL PRIMARY KEY,
    area_id INTEGER,
    area_attr_id INTEGER,
    parent_area_id INTEGER,
    area_short_code TEXT,
    area_long_code TEXT,
    area_name TEXT,
    area_desc TEXT,
    classification TEXT,
    classification_code TEXT,
    objectid INTEGER,
    geometry geometry(MultiPolygon, 4326)
);

CREATE TABLE parks (
    id SERIAL PRIMARY KEY,
    location_id INT,
    asset_id INT,
    name TEXT,
    type TEXT,
    amenities TEXT,
    address TEXT,
    phone TEXT,
    url TEXT,
    geometry GEOMETRY(Point, 4326)
);