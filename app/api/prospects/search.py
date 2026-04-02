from fastapi import APIRouter, Query
from typing import Optional
from app.utils.make_meta import make_meta
from app.utils.db import get_db_connection

router = APIRouter()

@router.get("/prospects/search")
def prospects_search(query: str = Query(..., description="Search query string"),
                    page: int = Query(1, ge=1, description="Page number (1-based)"),
                    limit: int = Query(50, ge=1, le=500, description="Records per page (default 50, max 500)")) -> dict:
    """Search prospects using full-text search on search_vector column, excluding hidden."""
    meta = make_meta("success", f"Search prospects for query: {query}")
    data = []
    total = 0
    if not query or not query.strip():
        meta = make_meta("error", "Query parameter is required for search.")
        return {"meta": meta, "data": [], "pagination": {"page": page, "limit": limit, "total": 0, "pages": 0}}
    conn_gen = get_db_connection()
    conn = next(conn_gen)
    cur = conn.cursor()
    offset = (page - 1) * limit
    try:
        # Count total matches
        cur.execute("SELECT COUNT(*) FROM prospects WHERE search_vector @@ plainto_tsquery('english', %s) AND hide IS NOT TRUE;", (query,))
        count_row = cur.fetchone() if cur.description is not None else None
        total = count_row[0] if count_row is not None else 0
        # Fetch paginated results
        cur.execute("SELECT * FROM prospects WHERE search_vector @@ plainto_tsquery('english', %s) AND hide IS NOT TRUE OFFSET %s LIMIT %s;", (query, offset, limit))
        if cur.description is not None:
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            data = [dict(zip(columns, row)) for row in rows]
        else:
            data = []
    except Exception as e:
        meta = make_meta("error", f"Search failed: {str(e)}")
        data = []
        total = 0
    finally:
        cur.close()
        conn.close()
    return {
        "meta": meta,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total // limit) + (1 if total % limit else 0)
        },
        "data": data,
    }
