import os
from dotenv import load_dotenv
from pathlib import Path

import psycopg2

DEBUG_MODE = True

# Load .env from parent directory
env_path = Path(__file__).resolve().parent.parent / "../.env"
load_dotenv(dotenv_path=env_path)

# Connect to the database
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}