def get_db_connection_direct():
    """Create and return a PostgreSQL connection (not a generator)."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():  # type: ignore[return]
    """Create and yield a PostgreSQL connection for use as a FastAPI dependency."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    try:
        yield conn
    finally:
        conn.close()
