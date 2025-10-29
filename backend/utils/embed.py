import os
from openai import OpenAI 

# --- Config ---
EMBED_DIM = 1536

# Intialize embedding client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generate Embedding
def embed_text(text: str):
    """ Returns an embedding vector for a string. """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding