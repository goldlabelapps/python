"""API route definitions for NX AI."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class EchoRequest(BaseModel):
    """Request body for the echo endpoint."""

    message: str


class EchoResponse(BaseModel):
    """Response body for the echo endpoint."""

    echo: str


@router.get("/")
def root() -> dict[str, str]:
    """Return a welcome message for the API root."""
    return {"message": "Welcome to NX AI!"}


@router.get("/health")
def health() -> dict[str, str]:
    """Return the health status of the application."""
    return {"status": "ok"}


@router.post("/echo", response_model=EchoResponse)
def echo(body: EchoRequest) -> EchoResponse:
    """Echo the provided message back to the caller."""
    return EchoResponse(echo=body.message)
