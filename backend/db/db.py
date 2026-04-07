import psycopg2
import psycopg2.extras
import psycopg2.pool
from contextlib import contextmanager

from config.settings import DB_CONFIG, DEBUG_MODE

# Connection pool
pool = psycopg2.pool.ThreadedConnectionPool(
        minconn = 1,
        maxconn = 10,
        **DB_CONFIG
)

@contextmanager
def get_conn():
    conn = pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SET search_path to data, public")
        yield conn
    finally:
        pool.putconn(conn) # Always return connection to pool

def execute_sql(sql: str):
    print(f"[DB] Attempting query: {sql}")
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            try:
                cur.execute(sql)
                return cur.fetchall()

            except Exception as e:
                if DEBUG_MODE:
                    print(f"(DEUBG)[DB] SQL execution failed: {e}")
                conn.rollback()
                return None
