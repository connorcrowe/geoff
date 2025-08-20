from fastapi import APIRouter, Request
from services import query_service

router = APIRouter()

@router.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    return query_service.handle_user_query(prompt)

@router.post("/manual_query")
async def handle_manual_query(req: Request):
    data = await req.json()
    sql = data.get("sql", "")
    return query_service.handle_manual_query(sql)