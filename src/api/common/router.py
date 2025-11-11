from typing import Literal

from fastapi import APIRouter, Request
from starsessions import load_session

router = APIRouter()


@router.get("/ping/")
def ping() -> Literal["Pong!"]:
    return "Pong!"


@router.post("/test/")
async def test(request: Request) -> dict[str, str]:
    await load_session(request)

    request.session["key"] = "value"

    session_data = request.session
    return session_data
