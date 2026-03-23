from app import __version__
import os, time
import csv
from fastapi import APIRouter, status
from app.api.db import get_db_connection

router = APIRouter()

CSV_PATH = os.path.join(os.path.dirname(__file__), 'start_data.csv')
CSV_PATH = os.path.abspath(CSV_PATH)

@router.get("/products/seed", status_code=status.HTTP_200_OK)
def seed_products() -> dict:
    """Delete and recreate the product table, then seed with CSV data."""
    conn_gen = get_db_connection()
    conn = next(conn_gen)
    cur = conn.cursor()
    # Drop and recreate table with all CSV columns
    cur.execute('''
        DROP TABLE IF EXISTS product;
        CREATE TABLE product (
            id SERIAL PRIMARY KEY,
            Params TEXT,
            item INTEGER,
            title TEXT,
            UOS TEXT,
            Pack_Description TEXT,
            Hierarchy1 TEXT,
            Hierarchy2 TEXT,
            Hierarchy3 TEXT,
            UOP TEXT,
            sSell1 NUMERIC(10,2),
            sSell2 NUMERIC(10,2),
            sSell3 NUMERIC(10,2),
            sSell4 NUMERIC(10,2),
            sSell5 NUMERIC(10,2),
            pack1 INTEGER,
            pack2 INTEGER,
            pack3 INTEGER,
            pack4 INTEGER,
            pack5 INTEGER,
            EAN TEXT
        );
    ''')
    # Read and insert CSV data
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
        for row in rows:
            # Map 'desc' from CSV to 'title' for DB
            row['title'] = row.pop('desc')
            cur.execute(
                """
                INSERT INTO product (
                    Params, item, title, UOS, Pack_Description, Hierarchy1, Hierarchy2, Hierarchy3, UOP,
                    sSell1, sSell2, sSell3, sSell4, sSell5, pack1, pack2, pack3, pack4, pack5, EAN
                ) VALUES (
                    %(Params)s, %(item)s, %(title)s, %(UOS)s, %(Pack_Description)s, %(Hierarchy1)s, %(Hierarchy2)s, %(Hierarchy3)s, %(UOP)s,
                    %(sSell1)s, %(sSell2)s, %(sSell3)s, %(sSell4)s, %(sSell5)s, %(pack1)s, %(pack2)s, %(pack3)s, %(pack4)s, %(pack5)s, %(EAN)s
                )
                """,
                row
            )
    conn.commit()
    cur.execute('SELECT * FROM product;')
    if cur.description is None:
        products = []
    else:
        columns = [desc[0] for desc in cur.description]
        products = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    epoch = int(time.time() * 1000)
    meta = {
        "severity": "success",
        "title": "Product table seeded",
        "version": __version__,
        "base_url": base_url,
        "time": epoch,
    }
    return {"meta": meta, "data": products}
