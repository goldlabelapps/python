"""NX AI - FastAPI entry point."""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="NX AI",
    description="A clean, modular FastAPI backend demonstrating Python expertise.",
    version="1.0.0",
)

app.include_router(router)
