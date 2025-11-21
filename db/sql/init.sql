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

-- Database Schemas
CREATE TABLE IF NOT EXISTS meta.schema_embeddings (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    column_name TEXT,
    col_type TEXT,
    description TEXT,
    embedding VECTOR(1536)
);

ALTER TABLE meta.schema_embeddings
ADD CONSTRAINT unique_table_column UNIQUE(table_name, column_name);

-- Example Queries
CREATE TABLE IF NOT EXISTS meta.example_embeddings (
    id SERIAL PRIMARY KEY,
    user_query TEXT NOT NULL,
    tables TEXT[] NOT NULL,
    components TEXT[] NOT NULL,
    plan JSONB NOT NULL,
    embedding vector(1536), 
    embedding_version INT NOT NULL DEFAULT 1,
    last_embedded TIMESTAMP,
    file_hash TEXT  -- stores hash of the JSON file for change detection
);