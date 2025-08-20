# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(title="Geoff", version="0.1")
app.include_router(router)

# Allow requests from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)



# @app.post("/manual_query")
# async def handle_manual_query(request: Request):
#     data = await request.json()
#     sql = data.get("sql", "")

    
#     rows, colnames, error = db.execute_sql(sql)
#     geojson, table_columns, table_rows = geo.convert_rows_to_geojson(rows, colnames)

#     return {
#         "sql": sql.strip(),
#         "geojson": geojson,
#         "columns": table_columns,
#         "rows": table_rows
#     }
