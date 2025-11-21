import os
import json 
import psycopg2
import hashlib

from openai import OpenAI
from psycopg2.extras import RealDictCursor

from utils.embed import embed

# --- Config ---
EMBED_DIM = 1536
EXAMPLES_PATH = "/app/examples/"
CURRENT_EMBEDDING_VERSION = 1

# Intialize embedding client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _connect():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def _file_hash_for_plan(user_query, plan, metadata):
    to_hash = {
        "user_query": user_query,
        "plan": plan,
        "metadata": metadata
    }
    hash_bytes = json.dumps(to_hash, sort_keys=True).encode("utf-8")
    return hashlib.sha256(hash_bytes).hexdigest()

def _load_example(path):
    with open(path, "r") as f:
        return json.load(f)

def _get_all_db_examples(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, file_hash FROM meta.example_embeddings;")
        rows = cur.fetchall()
        return {row["id"]: row for row in rows}

def insert_example(conn, example, file_hash, emb_vector):
    tables = example["metadata"]["tables"]
    components = example["metadata"]["components"]

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO meta.example_embeddings
                (id, user_query, tables, components, plan, embedding,
                 embedding_version, last_embedded, file_hash)
            VALUES
                (%s, %s, %s, %s, %s, %s,
                 %s, NOW(), %s)
            """,
            (
                example["id"],
                example["user_query"],
                tables,
                components,
                json.dumps(example["plan"]),
                emb_vector,
                CURRENT_EMBEDDING_VERSION,
                file_hash
            )
        )
    conn.commit()


def update_example(conn, example, file_hash, emb_vector):
    tables = example["metadata"]["tables"]
    components = example["metadata"]["components"]

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE meta.example_embeddings
            SET 
                user_query = %s,
                tables = %s,
                components = %s,
                plan = %s,
                embedding = %s,
                embedding_version = %s,
                last_embedded = NOW(),
                file_hash = %s
            WHERE id = %s
            """,
            (
                example["user_query"],
                tables,
                components,
                json.dumps(example["plan"]),
                emb_vector,
                CURRENT_EMBEDDING_VERSION,
                file_hash,
                example["id"]
            )
        )
    conn.commit()


def delete_example(conn, example_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM meta.example_embeddings WHERE id = %s", (example_id,))
    conn.commit()

def count_total(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM meta.example_embeddings")
        return cur.fetchone()[0]

if __name__ == "__main__":
    conn = _connect()
    db_snapshot = _get_all_db_examples(conn)

    created, updated, deleted = 0, 0, 0

    # Source all example files
    paths = []
    for root, dirs, files in os.walk(EXAMPLES_PATH):
        for fname in files:
            if fname.endswith(".json"):
                paths.append(os.path.join(root, fname))
    
    ids = set()

    for json_path in paths:
        example = _load_example(json_path)
        ex_id = example["id"]
        ids.add(ex_id)

        new_hash = _file_hash_for_plan(example["user_query"], example["plan"], example["metadata"])

        # Insert
        if ex_id not in db_snapshot:
            emb_vector = embed(example["user_query"], client)
            insert_example(conn, example, new_hash, emb_vector)
            created += 1
            continue

        # Exists, check hash
        old_hash = db_snapshot[ex_id]["file_hash"]
        if new_hash != old_hash:
            emb_vector = embed(example["user_query"], client)
            update_example(conn, example, new_hash, emb_vector)
            updated += 1
        
    # Deletions
    db_ids = set(db_snapshot.keys())
    removed_ids = db_ids - ids

    for ex_id in removed_ids:
        delete_example(conn, ex_id)
        deleted += 1

    total = count_total(conn)
    conn.close()


    print("\n=== Sync Summary ===")
    print(f"Created: {created}")
    print(f"Updated: {updated}")
    print(f"Deleted: {deleted}")
    print(f"Total in DB: {total}")