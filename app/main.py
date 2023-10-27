from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import api

app = FastAPI()
app.include_router(api.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
