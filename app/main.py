from typing import Literal

from fastapi import FastAPI
from pydantic import UUID4

from app.tasks import add_one

app = FastAPI()


@app.get("/ping")
async def ping() -> Literal["Pong!"]:
    return "Pong!"


@app.get("/run")
async def run() -> UUID4:
    result = add_one.delay(1)
    return UUID4(result.task_id)
