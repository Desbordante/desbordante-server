from typing import Literal

from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def ping() -> Literal["Pong!"]:
    return "Pong!"
