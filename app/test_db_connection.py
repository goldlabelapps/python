import os
import sys

import psycopg2
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()

    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    print("Attempting connection with:")
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"Database: {db_name}")
    print(f"User: {db_user}")

    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )
        print("Connection successful!")
        conn.close()
        return 0
    except Exception as e:
        print(f"Connection failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
