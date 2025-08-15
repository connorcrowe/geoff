from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from shapely import wkb

from llm import generate_sql_from_prompt

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# Allow requests from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Connect to the database
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Set the search_path for the connection
with conn.cursor() as cur:
    cur.execute("SET search_path TO data")
conn.commit()

def convert_rows_to_geojson(rows, colnames):
    # Identify geometry column (first that can be parsed as WKB)
    geom_index = None
    for i, name in enumerate(colnames):
        for r in rows:
            try:
                if r[i] is not None:
                    wkb.loads(r[i], hex=True)
                    geom_index = i
                    break
            except Exception: continue
        if geom_index is not None: break
     
    features = []
    table_rows = []
    for row in rows:
        props = {}
        geom = None

        for i, val in enumerate(row):
            if i == geom_index:
                try:
                    geom_obj = wkb.loads(val, hex=True) if val else None
                    geom = json.loads(json.dumps(geom_obj.__geo_interface__)) if geom_obj else None
                except Exception:
                    geom = None
            else:
                props[colnames[i]] = val

        if geom:
            features.append({
                "type": "Feature",
                "geometry": geom,
                "properties": props
            })

        table_rows.append([props.get(c) if c in props else row[colnames.index(c)] for c in colnames if colnames.index(c) != geom_index])

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Remove geometry column from table header
    table_columns = [c for i, c in enumerate(colnames) if i != geom_index]
    return geojson, table_columns, table_rows

def generate_and_run_sql(user_prompt: str, max_retries: int=2):
    attempts = 0
    sql = generate_sql_from_prompt(user_prompt)

    while attempts <= max_retries:
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return rows, colnames, sql, None
        except Exception as e:
            print("(MAIN)[ERROR] Returned SQL does not execute. Reattempting.")
            conn.rollback()
            attempts += 1
            if attempts > max_retries:
                return None, None, sql, str(e)
            
            # Try again with corrective prompt
            sql = generate_sql_from_prompt(user_prompt, previous_sql=sql, error_message=str(e))

@app.post("/query")
async def handle_user_query(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "")

    rows, colnames, sql, error = generate_and_run_sql(user_prompt)
    if error:
        return {"error": error, "sql": sql}

    geojson, table_columns, table_rows = convert_rows_to_geojson(rows, colnames)
    return {
        "sql": sql.strip(),
        "geojson": geojson,
        "columns": table_columns,
        "rows": table_rows
    }