import psycopg2

from config.settings import DB_CONFIG, DEBUG_MODE

# Persistent connection
conn = psycopg2.connect(**DB_CONFIG)

# Set schema search path
with conn.cursor() as cur:
    cur.execute("SET search_path TO data, public")
conn.commit()

def execute_sql(sql: str):
    """Executes SQL and catches errors, rolling back if necessary."""
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            return rows, colnames, None

        except Exception as e:
            if DEBUG_MODE:
                print(f"(DEUBG)[DB] SQL execution failed: {e}")
            conn.rollback()
            return None, None, str(e)