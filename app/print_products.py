import os

import psycopg2
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM product;')
        rows = cur.fetchall()
        for row in rows:
            print(row)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
