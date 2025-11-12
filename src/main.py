import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starsessions import SessionMiddleware

from src.api import router as api_router
from src.domain.session.config import settings as session_settings
from src.exceptions import BaseAppException
from src.infrastructure.lock import lock_manager
from src.infrastructure.rate_limit.limiter import limiter
from src.infrastructure.session.manager import session_manager
from src.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await lock_manager.destroy()
    await session_manager.close()


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

app.add_middleware(
    SessionMiddleware,
    store=session_manager.get_store(),
    cookie_name=session_settings.COOKIE_NAME,
    cookie_https_only=session_settings.COOKIE_HTTPS_ONLY,
    lifetime=session_settings.LIFETIME,
    rolling=session_settings.ROLLING,
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
