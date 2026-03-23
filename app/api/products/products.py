
from app import __version__
from fastapi import APIRouter
import os, time
from app.api.db import get_db_connection

router = APIRouter()

@router.get("/products")
def root() -> dict:
    """Return all products with full CSV-based schema."""
    conn_gen = get_db_connection()
    conn = next(conn_gen)
    cur = conn.cursor()
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
        "title": "Product List",
        "version": __version__,
        "base_url": base_url,
        "time": epoch,
    }
    return {"meta": meta, "data": products}
