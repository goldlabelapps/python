
from app import __version__

import os
from app.utils.make_meta import make_meta
from fastapi import APIRouter, Query, Path
from app.utils.db import get_db_connection

router = APIRouter()
base_url = os.getenv("BASE_URL", "http://localhost:8000")

@router.get("/prompts")
def root() -> dict:
    """GET /prompts endpoint."""
    from fastapi import status
    meta = None
    data = []
    # Check if 'prompts' table exists
    from app.utils.db import get_db_connection_direct
    conn = get_db_connection_direct()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'prompts'
                );
            """)
            result = cur.fetchone()
            exists = result[0] if result else False
    finally:
        conn.close()
    if not exists:
        meta = make_meta("warning", "Table 'prompts' does not exist.")
        # Do not include 'kata' key or any other keys in data
        response = {"meta": meta}
    else:
        meta = make_meta("success", "Prompts endpoint")
        # Example: include 'kata' key only if table exists (add as needed)
        data = [
            {"init": f"{base_url}/prompts", "kata": "example"},
        ]
        response = {"meta": meta, "data": data}
    # Remove 'kata' key from all items in data if table does not exist
    if not exists:
        for item in data:
            item.pop('kata', None)
    return response
