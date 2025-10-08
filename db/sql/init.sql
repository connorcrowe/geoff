CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS data;
CREATE SCHEMA IF NOT EXISTS meta;

CREATE TABLE IF NOT EXISTS meta.datasets (
    dataset_name text PRIMARY KEY,
    source_url text,
    last_ingested timestamptz,
    last_loaded timestamptz
);