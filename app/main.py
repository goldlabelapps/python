from app import __version__
"""NX AI - FastAPI entry point."""


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app import __version__
from app.api.routes import router

app = FastAPI(
    title="NX AI",
    description="Production-ready Python FastAPI app for NX",
    version=__version__,
)


app.include_router(router)

# Mount static directory
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    return FileResponse(favicon_path)
