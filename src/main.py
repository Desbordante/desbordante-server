import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.sessions import SessionMiddleware

from src.api import router as api_router
from src.domain.security.config import settings as security_settings
from src.exceptions import BaseAppException
from src.infrastructure.lock import lock_manager
from src.infrastructure.rate_limit.limiter import limiter
from src.infrastructure.redis.config import settings as redis_settings
from src.infrastructure.storage.client import create_s3_storage
from src.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis.from_url(
        redis_settings.redis_sessions_dsn.unicode_string(), decode_responses=True
    )
    app.state.redis = redis

    app.state.storage = create_s3_storage()

    yield
    await redis.aclose()
    await lock_manager.destroy()


app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    redirect_slashes=False,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware for Authlib
app.add_middleware(
    SessionMiddleware,
    secret_key=security_settings.SECRET_KEY.get_secret_value(),
    max_age=None,
)


# Global exception handlers
@app.exception_handler(BaseAppException)
def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(api_router)
