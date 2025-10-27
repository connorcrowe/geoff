# Generate Embedding
def embed(text: str, client):
    """ Returns an embedding vector for a string. """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding