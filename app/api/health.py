from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health() -> dict[str, str]:
    """Return the health status of the application."""
    return {"status": "ok"}
