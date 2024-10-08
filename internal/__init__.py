from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from internal.rest import http
from internal.rest.http.exception import add_exception_handlers

app = FastAPI()
app.include_router(http.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_exception_handlers(app)
