"""NX AI - FastAPI entry point."""

from fastapi import FastAPI

from app import __version__
from app.api.routes import router

app = FastAPI(
    title="NX AI",
    description="Production-ready Python FastAPI app for NX",
    version=__version__,
)

app.include_router(router)
