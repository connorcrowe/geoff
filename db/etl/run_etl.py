import os
import importlib
from datetime import datetime
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Auto-discover all dataset modules
def get_dataset_modules():
    files = [file[:-3] for file in os.listdir("datasets") if file.endswith(".py")]
    modules = [importlib.import_module(f"datasets.{name}") for name in files]
    
    print(f"[ETL]: Discovered modules:\n{modules}")
    return modules

# Write dataframe to STAGING and update META
def write_staging_with_meta(df, table_name, source_url):
    df.to_sql(table_name, engine, schema="staging", if_exists="replace", index=False)

    # Metadata update
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO meta.datasets (dataset_name, source_url, last_ingested)
                VALUES (:name, :url, :ts)
                ON CONFLICT (dataset_name) DO UPDATE
                SET last_ingested = :ts
            """),
            {"name": table_name, "url": source_url, "ts": datetime.utcnow()}
        )
        print(f"[ETL|{table_name}] Written to staging and metadata updated ({len(df)} records)")

# INGEST
def ingest_one(dataset_name):
    print(f"[ETL]: Ingesting just {dataset_name}...")
    module = importlib.import_module(f"datasets.{dataset_name}")
    df, table_name, source_url = module.fetch()
    write_staging_with_meta(df, table_name, source_url)

def ingest_all():
    for module in get_dataset_modules():
        print(f"[ETL]: Starting ingest of {module.__name__} ...")
        df, table_name, source_url = module.fetch()
        write_staging_with_meta(df, table_name, source_url)

# LOAD
def load_one(dataset_name):
    print(f"[ETL]: Transforming just {dataset_name} ...")
    sql_file = dataset_name + ".sql"
    with open(os.path.join("transform", sql_file)) as file:
                with engine.connect() as conn:
                    conn.execute(text(file.read()))
                    conn.commit()

def load_all():
    for sql_file in os.listdir("transform"):
        if sql_file.endswith(".sql"):
            print(f"[ETL]: Starting transform of {sql_file} ...")
            with open(os.path.join("transform", sql_file)) as file:
                with engine.connect() as conn:
                    conn.execute(text(file.read()))
                    conn.commit()

if __name__ == "__main__":
    import sys

    command = sys.argv[1]

    if command == "ingest":
        if len(sys.argv) == 2:
            ingest_all()
        elif len(sys.argv) == 3:
            ingest_one(sys.argv[2])
        else:
            print("Usage: python run_etl.py ingest [dataset_name]")
            sys.exit(1)
    elif command == "load":
        if len(sys.argv) == 2:
            load_all()
        elif len(sys.argv) == 3:
            load_one(sys.argv[2])
        else:
            print("Usage: python run_etl.py load [dataset_name]")
            sys.exit(1)