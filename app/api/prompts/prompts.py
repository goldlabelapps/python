from fastapi import HTTPException
from app import __version__

import os
from app.utils.make_meta import make_meta
from fastapi import APIRouter, Query, Path, status
from app.utils.db import get_db_connection
from app.api.prompts.schemas import PromptCreate, PromptOut
from fastapi import Body

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
        return {"meta": meta}
    else:
        meta = make_meta("success", "Prompts")
        # Fetch all records from prompts table
        data = []
        conn = get_db_connection_direct()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, prompt, response, llm, started, completed, timestamp FROM prompts ORDER BY id DESC;")
                rows = cur.fetchall()
                keys = ["id", "prompt", "response", "llm", "started", "completed", "timestamp"]
                for row in rows:
                    data.append(dict(zip(keys, row)))
        finally:
            conn.close()
        return {"meta": meta, "data": data}
    


# POST /prompts endpoint
@router.post("/prompts", status_code=status.HTTP_201_CREATED)
def create_prompt(prompt_in: PromptCreate = Body(...)):
    """Create a new prompt record in the prompts table."""
    from app.utils.db import get_db_connection_direct
    import psycopg2
    import time
    conn = get_db_connection_direct()
    started = prompt_in.started if prompt_in.started is not None else int(time.time())
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO prompts (prompt, response, llm, started, completed, timestamp)
                VALUES (%s, %s, %s, %s, %s, COALESCE(%s, NOW()))
                RETURNING id, prompt, response, llm, started, completed, timestamp
                """,
                (
                    prompt_in.prompt,
                    None,  # Always set response to NULL initially
                    prompt_in.llm,
                    started,
                    None,  # completed is NULL initially
                    None,  # timestamp
                )
            )
            row = cur.fetchone()
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
    if row:
        keys = ["id", "prompt", "response", "llm", "started", "completed", "timestamp"]
        return dict(zip(keys, row))
    return {"error": "Failed to insert prompt."}


# DELETE /prompts/{id} endpoint
@router.delete("/prompts/{id}", status_code=status.HTTP_200_OK)
def delete_prompt(id: int):
    """Delete a prompt record by id from the prompts table."""
    from app.utils.db import get_db_connection_direct
    import psycopg2
    conn = get_db_connection_direct()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM prompts WHERE id = %s RETURNING id;", (id,))
            row = cur.fetchone()
            conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    if row:
        return {"success": True, "deleted_id": row[0]}
    raise HTTPException(status_code=404, detail=f"Prompt with id {id} not found.")
