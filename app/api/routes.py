"""API route definitions for NX AI."""

import os
import time

import psycopg2
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app import __version__

load_dotenv()

router = APIRouter()


def get_db_connection():  # type: ignore[return]
    """Create and yield a PostgreSQL connection for use as a FastAPI dependency."""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
    )
    try:
        yield conn
    finally:
        conn.close()


class EchoRequest(BaseModel):
    """Request body for the echo endpoint."""

    message: str


class EchoResponse(BaseModel):
    """Response body for the echo endpoint."""

    echo: str


@router.get("/")
def root(conn=Depends(get_db_connection)) -> dict:
    """Return a structured welcome message for the API root, including product data."""
    cur = conn.cursor()
    try:
        cur.execute('SELECT id, name, description, price, in_stock, created_at FROM product;')
        products = [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "price": str(row[3]) if row[3] is not None else None,
                "in_stock": row[4],
                "created_at": row[5].isoformat() if row[5] else None,
            }
            for row in cur.fetchall()
        ]
    finally:
        cur.close()
    epoch = int(time.time() * 1000)
    meta = {
        "version": __version__,
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "epoch": epoch,
        "severity": "success",
        "message": f"NX AI says hello. Returned {len(products)} products.",
    }
    return {"meta": meta, "data": products}


@router.get("/health")
def health() -> dict[str, str]:
    """Return the health status of the application."""
    return {"status": "ok"}


@router.post("/echo", response_model=EchoResponse)
def echo(body: EchoRequest) -> EchoResponse:
    """Echo the provided message back to the caller."""
    return EchoResponse(echo=body.message)
