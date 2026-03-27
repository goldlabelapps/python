from app import __version__
import os
from app.utils.make_meta import make_meta
from fastapi import APIRouter
from app.utils.db import get_db_connection

router = APIRouter()


@router.get("/prospects")
def root() -> dict:
    """Return a placeholder message for prospects endpoint."""
    meta = make_meta("success", "Prospects placeholder")
    data = {"message": "This is a placeholder for the /prospects endpoint."}
    return {"meta": meta, "data": data}


# New endpoint: /prospects/init

@router.get("/prospects/init")
def prospects_init() -> dict:
    """Initialize prospects and return real total count."""
    meta = make_meta("success", "Initialized prospects")
    conn_gen = get_db_connection()
    conn = next(conn_gen)
    cur = conn.cursor()
    title = []
    total_unique_title = 0
    seniority = []
    total_unique_seniority = 0
    sub_departments = []
    total_unique_sub_departments = 0
    try:
        cur.execute('SELECT COUNT(*) FROM prospects;')
        row = cur.fetchone()
        total = row[0] if row is not None else 0

        # Get unique titles and their counts (column is 'title')
        cur.execute('SELECT title, COUNT(*) FROM prospects WHERE title IS NOT NULL GROUP BY title ORDER BY COUNT(*) DESC;')
        title_rows = cur.fetchall()
        title = [
            {"label": t[0], "count": t[1]} for t in title_rows if t[0] is not None
        ]
        total_unique_title = len(title)

        # Get unique seniority and their counts (column is 'seniority')
        cur.execute('SELECT seniority, COUNT(*) FROM prospects WHERE seniority IS NOT NULL GROUP BY seniority ORDER BY COUNT(*) DESC;')
        seniority_rows = cur.fetchall()
        seniority = [
            {"label": s[0], "count": s[1]} for s in seniority_rows if s[0] is not None
        ]
        total_unique_seniority = len(seniority)

        # Get unique sub_departments and their counts (column is 'sub_departments')
        cur.execute('SELECT sub_departments, COUNT(*) FROM prospects WHERE sub_departments IS NOT NULL GROUP BY sub_departments ORDER BY COUNT(*) DESC;')
        sub_department_rows = cur.fetchall()
        sub_departments = [
            {"label": sd[0], "count": sd[1]} for sd in sub_department_rows if sd[0] is not None
        ]
        total_unique_sub_departments = len(sub_departments)
    except Exception:
        total = 0
        title = []
        total_unique_title = 0
        seniority = []
        total_unique_seniority = 0
        sub_departments = []
        total_unique_sub_departments = 0
    finally:
        cur.close()
        conn.close()
    data = {
        "total_prospects": total,
        "title": {
            "total_unique": total_unique_title,
            "values": title
        },
        "seniority": {
            "total_unique": total_unique_seniority,
            "values": seniority
        },
        "departments": {
            "total_unique": total_unique_sub_departments,
            "values": sub_departments
        }
    }
    return {"meta": meta, "data": data}
