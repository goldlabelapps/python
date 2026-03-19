from app import __version__
"""API route definitions for NX AI."""

import os
import time

import psycopg2
from dotenv import load_dotenv

from fastapi import APIRouter, Depends

from app.api.db import get_db_connection
from app.api.schemas import EchoRequest, EchoResponse

router = APIRouter()

from app.api.root import router as root_router
from app.api.health import router as health_router
from app.api.echo import router as echo_router

router.include_router(root_router)
router.include_router(health_router)
router.include_router(echo_router)





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
