from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router

app = FastAPI(generate_unique_id_function=lambda route: route.name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
