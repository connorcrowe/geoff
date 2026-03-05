from fastapi import APIRouter, Request
from fastapi.responses import Response
from services import query_service
from services import layer_store
from core import mvt_builder

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

@router.get("/tiles/{layer_id}/{z}/{x}/{y}.pbf")
async def get_tile(layer_id: str, z: int, x: int, y: int):
    # Retrieve the stored query for this layer
    print(f"[Route] Requesting {layer_id}, {z}, {x}, {y}")
    layer_data = layer_store.get_layer(layer_id)
    
    if not layer_data:
        print(f"[Route] Route {layer_id} not found")
        return Response(
            content=b"",
            status_code=404,
            media_type="application/x-protobuf"
        )
    
    base_query = layer_data["sql"]
    layer_name = layer_data["name"]
    
    # Build MVT query for this specific tile
    mvt_query = mvt_builder.build_mvt_query(base_query, layer_name, z, x, y)
    
    # Execute query to get MVT binary data
    rows = execute_sql(mvt_query)
    
    if not rows or not rows[0].get("mvt"):
        # No features in this tile - return empty tile
        return Response(
            content=b"",
            status_code=204,
            media_type="application/x-protobuf"
        )
    
    # Return the MVT binary data
    mvt_data = bytes(rows[0]["mvt"])
    print(f"[Route] mvt_data length: {len(mvt_data)}")
    
    return Response(
        content=mvt_data,
        media_type="application/x-protobuf",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=3600"  # Cache tiles for 1 hour
        }
    )