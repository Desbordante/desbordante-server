from fastapi import APIRouter

from src.api.auth.routes.github_authorize import router as github_authorize_router
from src.api.auth.routes.github_callback import router as github_callback_router
from src.api.auth.routes.google_authorize import router as google_authorize_router
from src.api.auth.routes.google_callback import router as google_callback_router

router = APIRouter()

router.include_router(github_authorize_router)
router.include_router(github_callback_router)
router.include_router(google_authorize_router)
router.include_router(google_callback_router)
