from fastapi import APIRouter, Request
from services import query_service

from db.db import execute_sql

router = APIRouter()

@router.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    return query_service.handle_user_query(prompt)

# @router.post("/manual_query")
# async def handle_manual_query(req: Request):
#     data = await req.json()
#     sql = data.get("sql", "")
#     return query_service.handle_manual_query(sql)

@router.get("/examples")
async def get_examples(limit: int=999):
    sql = f"SELECT user_query FROM meta.example_embeddings LIMIT {limit};"
    rows = execute_sql(sql)
    return rows

@router.get("/schemas")
async def get_schemas():
    sql = f"SELECT table_name, column_name, col_type, description FROM meta.schema_embeddings ORDER BY table_name, column_name;"
    rows = execute_sql(sql)
    
    schemas = {}
    for row in rows: 
        table = row["table_name"]
        column = {
            "column_name": row["column_name"],
            "column_type": row["col_type"],
            "description": row["description"]
        }
        schemas.setdefault(table, []).append(column)

    return schemas