from fastapi import APIRouter
from app.api.schemas import EchoRequest, EchoResponse

router = APIRouter()

@router.post("/echo", response_model=EchoResponse)
def echo(body: EchoRequest) -> EchoResponse:
    return EchoResponse(echo=body.message)
