import os
import psycopg2
from openai import OpenAI 

from utils.embed import embed

# --- Config ---
EMBED_DIM = 1536

# Connect to DB
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# Intialize embedding client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Query
cur.execute(
    """
    SELECT 
        table_schema,
        table_name,
        column_name,
        data_type,
        col_description(format('%I.%I', table_schema, table_name)::regclass::oid, ordinal_position) AS description
    FROM information_schema.columns
    WHERE table_schema='data'; 
    """
)
columns = cur.fetchall()

# Create embedding row
for schema, table, column, col_type, desc in columns:
    if col_type == "USER-DEFINED": col_type = "geometry"
    description = desc 
    text_to_embed = f"{table}.{column}: {description} (type: {col_type})"
    vector = embed(text_to_embed, client)

    cur.execute("""
        INSERT INTO meta.schema_embeddings (table_name, column_name, col_type, description, embedding)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (table_name, column_name) DO UPDATE
        SET description = EXCLUDED.description,
            col_type = EXCLUDED.col_type,
            embedding = EXCLUDED.embedding
    """, (table, column, col_type, description, vector))

# Close
conn.commit()
cur.close()
conn.close()
print(f"Embedded {len(columns)} columns.")