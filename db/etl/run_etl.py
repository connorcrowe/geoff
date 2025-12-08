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
def ingest_all_datasets():
    files = [file[:-3] for file in os.listdir("datasets") if file.endswith(".py")]
    for dataset_name in files:
        ingest_one_dataset(dataset_name)

def ingest_one_dataset(dataset_name):
    print(f"[ETL]: Ingesting {dataset_name}...")
    module = importlib.import_module(f"datasets.{dataset_name}")
    dfs, table_name, source_url = module.fetch()

    if isinstance(dfs, dict): multi_table_ingest(dataset_name, dfs, table_name, source_url)
    else: ingest_dataset_multi_table(dataset_name, dfs, table_name, source_url)

def ingest_dataset_single_table(dataset_name, df, table_name, source_url):
    write_staging_with_meta(df, table_name, source_url)

def ingest_dataset_multi_table(dataset_name, dfs, table_prefix, source_url):
    for name, df in dfs.items():
        cleaned = name.replace(".txt", "").lower()
        full_name = f"{table_prefix}_{cleaned}"
        print(f"- [ETL]: Ingesting sub table {full_name}")
        write_staging_with_meta(df, full_name, source_url)

# LOAD
def load_all_datasets():
    files = [file[:-4] for file in os.listdir("transform") if file.endswith(".sql")]
    for dataset_name in files:
        load_one_dataset(dataset_name)

def load_one_dataset(dataset_name):
    print(f"[ETL]: Loading {dataset_name} ...")
    sql_file = dataset_name + ".sql"
    with open(os.path.join("transform", sql_file)) as file:
                with engine.connect() as conn:
                    conn.execute(text(file.read()))
                    conn.commit()

if __name__ == "__main__":
    import sys

    command = sys.argv[1]

    if command == "ingest":
        if len(sys.argv) == 2:
            ingest_all_datasets()
        elif len(sys.argv) == 3:
            ingest_one_dataset(sys.argv[2])
        else:
            print("Usage: python run_etl.py ingest [dataset_name]")
            sys.exit(1)
    elif command == "load":
        if len(sys.argv) == 2:
            load_all_datasets()
        elif len(sys.argv) == 3:
            load_one_dataset(sys.argv[2])
        else:
            print("Usage: python run_etl.py load [dataset_name]")
            sys.exit(1)