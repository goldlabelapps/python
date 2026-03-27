from app import __version__
import os
from app.utils.make_meta import make_meta
from fastapi import APIRouter
from app.utils.db import get_db_connection

router = APIRouter()


# Endpoint to get unique values for specified fields
from fastapi import Query

@router.get("/prospects/unique")
def get_unique_fields(fields: list[str] = Query(..., description="List of field names to get unique values for")) -> dict:
    """Return lists of unique values and their counts for specified fields in the prospects table."""
    conn_gen = get_db_connection()
    conn = next(conn_gen)
    cur = conn.cursor()
    result = {}
    errors = {}
    try:
        for field in fields:
            try:
                cur.execute(f'SELECT "{field}", COUNT(*) FROM prospects WHERE "{field}" IS NOT NULL GROUP BY "{field}" ORDER BY COUNT(*) DESC;')
                values = [
                    {"value": row[0], "count": row[1]} for row in cur.fetchall()
                ]
                result[field] = values
            except Exception as e:
                errors[field] = str(e)
        meta = make_meta("success", f"Unique values and counts for fields: {fields}")
        return {"meta": meta, "data": result, "errors": errors if errors else None}
    finally:
        cur.close()
        conn.close()


@router.get("/prospects")
def root() -> dict:
    """Return all prospects table records"""
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    conn_gen = get_db_connection()
    conn = next(conn_gen)
    cur = conn.cursor()
    actions = [
        {
            "name": "Seed prospects table",
            "url": f"{base_url}/prospects/seed"
        },
        {
            "name": "Empty prospects table",
            "url": f"{base_url}/prospects/empty"
        },
    ]
    try:
        cur.execute('SELECT * FROM prospects LIMIT 200;')
        if cur.description is None:
            prospects = []
        else:
            columns = [desc[0] for desc in cur.description]
            prospects = [dict(zip(columns, row)) for row in cur.fetchall()]
        meta = make_meta("success", "Prospects List (max 200)")
        result = {"meta": meta, "data": prospects}
    except Exception as e:
        import psycopg2
        if isinstance(e, psycopg2.errors.UndefinedTable):
            meta = make_meta("error", "prospects table does not exist.")
            result = {"meta": meta, "data": actions}
        else:
            meta = make_meta("error", str(e))
            result = {"meta": meta, "data": actions}
    finally:
        cur.close()
        conn.close()
    return result


# New endpoint: /prospects/init
@router.get("/prospects/init")
def prospects_init() -> dict:
    """Initialize prospects (placeholder endpoint)"""
    meta = make_meta("success", "Initialized prospects (placeholder)")
    data = {"message": "This is a placeholder for prospects/init."}
    return {"meta": meta, "data": data}
