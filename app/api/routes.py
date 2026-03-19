"""API route definitions for NX AI."""

from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import psycopg2
router = APIRouter()


router = APIRouter()


class EchoRequest(BaseModel):
    """Request body for the echo endpoint."""

    message: str


class EchoResponse(BaseModel):
    """Response body for the echo endpoint."""

    echo: str



import time
import sys
from app import __version__

@router.get("/")
def root() -> dict:
    """Return a structured welcome message for the API root, including product data."""
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price, in_stock, created_at FROM product;')
    products = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": float(row[3]),
            "in_stock": row[4],
            "created_at": row[5].isoformat() if row[5] else None
        }
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    epoch = int(time.time() * 1000)
    meta = {
        "version": __version__,
        "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "epoch": epoch,
        "severity": "success",
        "message": f"NX AI says hello. Returned {len(products)} products."
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
