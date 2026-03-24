from fastapi import APIRouter, status
import os, csv, time
from app.api.db import get_db_connection
from app import __version__
from app.utils.make_meta import make_meta

router = APIRouter()

@router.get("/products/update", status_code=status.HTTP_202_ACCEPTED)

def update_products() -> dict:
    meta = make_meta("info", "Product update from big_data.csv started")
    return {"meta": meta, "data": {
        "prompt": "We POST a CSV to this endpoint"
    }}