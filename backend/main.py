from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import psycopg2

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
        # Roll back failed transaction
        print("MAIN: Failed, rolling back databse")
        conn.rollback()
        return {"error": str(e), "sql": sql}

    #print("CUR[0]: ", cur.fetchall()[0])

    features = []
    for row in cur.fetchall():
        try:
            geom = wkb.loads(row[0], hex=True)
            geojson_geom = json.loads(json.dumps(geom.__geo_interface__))

            features.append({
                "type": "Feature",
                "geometry": geojson_geom,
                "properties": {}
            })
        except Exception as e:
            print("Skipping row due to error:", e)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    print ("Main Returning:")
    print("sql: ", sql)
    #print("geojson: ", geojson)

    return {
        "sql": sql.strip(),
        "geojson": geojson
    }
