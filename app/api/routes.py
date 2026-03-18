"""API route definitions for EchoApp."""

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
    return {"message": "Welcome to EchoApp!"}


@router.get("/health")
def health() -> dict[str, str]:
    """Return the health status of the application."""
    return {"status": "ok"}


@router.post("/echo", response_model=EchoResponse)
def echo(body: EchoRequest) -> EchoResponse:
    """Echo the provided message back to the caller."""
    return EchoResponse(echo=body.message)
