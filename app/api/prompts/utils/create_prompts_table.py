import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from app.utils.db import get_db_connection_direct

def run_create_prompts_table_sql():
    sql_path = os.path.join(os.path.dirname(__file__), "create_prompts_table.sql")
    with open(sql_path, "r") as f:
        sql = f.read()
    conn = get_db_connection_direct()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
        print("prompts table created or already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    run_create_prompts_table_sql()
