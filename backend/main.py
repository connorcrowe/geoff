from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from llm import prompt_to_sql
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from shapely import wkb

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

@app.post("/query")
async def run_query(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    sql = prompt_to_sql(prompt)

    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        conn.rollback()
        return {"error": str(e), "sql": sql}

    colnames = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    # Identify geometry column (first that can be parsed as WKB)
    geom_index = None
    for i, name in enumerate(colnames):
        for r in rows:
            try:
                if r[i] is not None:
                    wkb.loads(r[i], hex=True)
                    geom_index = i
                    break
            except Exception:
                continue
        if geom_index is not None:
            break

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

    return {
        "sql": sql.strip(),
        "geojson": geojson,
        "columns": table_columns,
        "rows": table_rows
    }
