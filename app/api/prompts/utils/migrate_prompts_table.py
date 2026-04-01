"""
Python migration script to update prompts table:
- Remove duration_ms column
- Add started (BIGINT NOT NULL, default now as epoch)
- Add completed (BIGINT, nullable)
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

ALTER_SQL = """
ALTER TABLE prompts
    DROP COLUMN IF EXISTS duration_ms,
    ADD COLUMN IF NOT EXISTS started BIGINT NOT NULL DEFAULT (extract(epoch from now())),
    ADD COLUMN IF NOT EXISTS completed BIGINT;
"""

def main():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(ALTER_SQL)
            conn.commit()
            print("Migration applied successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
