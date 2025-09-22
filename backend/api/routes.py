from fastapi import APIRouter, Request
from services import query_service
from config.examples import examples
from config.schemas import get_parsed_schemas

router = APIRouter()

@router.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    client_id = req.client.host
    return query_service.handle_user_query(prompt, client_id=client_id)

# @router.post("/manual_query")
# async def handle_manual_query(req: Request):
#     data = await req.json()
#     sql = data.get("sql", "")
#     return query_service.handle_manual_query(sql)

@router.get("/examples")
async def get_examples():
    return examples

@router.get("/schemas")
async def get_schemas():
    return get_parsed_schemas()