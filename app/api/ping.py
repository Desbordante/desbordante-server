from typing import Literal

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def ping() -> Literal["Pong"]:
    return "Pong"
