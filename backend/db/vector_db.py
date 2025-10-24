from collections import defaultdict

from db.db import execute_sql

def select_relevant_tables(embedding, score_threshold: float=-0.3):
    matches = query_table_embeddings(embedding, limit=100)

    # Filter on embed distance
    filtered = [m for m in matches if m["score"] <= score_threshold]

    # Group cols by table
    tables = defaultdict(list)
    for m in filtered:
        tables[m["table_name"]].append({
            "column_name": m["column_name"],
            "col_type": m["col_type"],
            "description": m["description"]
        })

    # Build list of tables sorted by relevance
    relevant_tables = sorted(
        [{"table_name": t, "columns": cols} for t, cols in tables.items()],
        key=lambda t: min(
            next((c for c in filtered if c["column_name"] == col["column_name"]), {"score": 0})["score"]
            for col in t["columns"]
        )
    )

    return relevant_tables

def query_table_embeddings(embedding, limit: int=999):
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    
    sql = f"""
    SELECT table_name, column_name, col_type, description, 
        embedding <#> '{embedding_str}' AS distance
    FROM meta.schema_embeddings
    ORDER BY distance ASC
    LIMIT {limit};
    """

    rows = execute_sql(sql)

    return [
        {
            "table_name": r["table_name"],
            "column_name": r["column_name"],
            "col_type": r["col_type"],
            "description": r["description"],
            "score": r["distance"]
        }
        for r in rows
    ]

