import os
import importlib
from datetime import datetime
from sqlalchemy import create_engine, text

user = os.getenv("POSTGRES_USER")
pwd = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("DB_HOST", "db")
port = os.getenv("DB_PORT", "5432")
db = os.getenv("POSTGRES_DB")

engine = create_engine(f"postgresql://{user}:{pwd}@{host}:{port}/{db}")

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

def single_table_ingest(dataset_name, df, table_name, source_url):
    write_staging_with_meta(df, table_name, source_url)

def multi_table_ingest(dataset_name, dfs, table_prefix, source_url):
    for name, df in dfs.items():
        cleaned = name.replace(".txt", "").lower()
        full_name = f"{table_prefix}_{cleaned}"
        print(f"- [ETL]: Ingesting sub table {full_name}")
        write_staging_with_meta(df, full_name, source_url)


# INGEST
def ingest_one(dataset_name):
    print(f"[ETL]: Ingesting {dataset_name}...")
    module = importlib.import_module(f"datasets.{dataset_name}")
    dfs, table_name, source_url = module.fetch()

    if isinstance(dfs, dict): multi_table_ingest(dataset_name, dfs, table_name, source_url)
    else: single_table_ingest(dataset_name, dfs, table_name, source_url)

def ingest_all():
    for module in get_dataset_modules():
        ingest_one(module)

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