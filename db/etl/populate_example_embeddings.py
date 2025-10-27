import os
import json 
import psycopg2
from openai import OpenAI

from utils.embed import embed
from examples.examples import examples_embedded, examples_pending_embed

# --- Config ---
EMBED_DIM = 1536
EXAMPLES_PATH = "/app/examples/examples.py"

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

len_prev_ex = len(examples_embedded)
len_to_embed = len(examples_pending_embed)

count = 0
for ex in examples_pending_embed[:]:
    user_query = ex["user_query"]
    example_type = ex["type"]
    sources = ex["sources"]
    plan = ex["plan"]
    
    # Embed
    emb_vector = embed(user_query, client)

    # Store in vector db
    cur.execute(
        """
        INSERT INTO meta.example_embeddings (type, sources, user_query, plan, embedding)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (example_type, sources, user_query, json.dumps(plan), emb_vector)
    )

    # Remove from exampels_pending_embed, add to examples_embedded
    examples_embedded.append(ex)
    examples_pending_embed.remove(ex)
    count += 1

# Commit DB changes
conn.commit()
cur.close()
conn.close()

# --- Write back to examples.py ---
with open(EXAMPLES_PATH, "w") as f:
    f.write("examples_embedded = ")
    f.write(json.dumps(examples_embedded, indent=4))
    f.write("\n\nexamples_pending_embed = ")
    f.write(json.dumps(examples_pending_embed, indent=4))
    f.write("\n")

print(f"✅ Embedded {count} examples. New total: {len(examples_embedded)}")