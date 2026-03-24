
from app import __version__
from app.utils.make_meta import make_meta
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

    meta = make_meta("success", "Product List")
    return {"meta": meta, "data": products}
