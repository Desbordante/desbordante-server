import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from src.api import router as api_router
from src.domain.security.config import settings
from src.exceptions import BaseAppException
from src.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    generate_unique_id_function=lambda route: route.name, redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY.get_secret_value())


# Global exception handlers
@app.exception_handler(BaseAppException)
def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(api_router)
