from fastapi import APIRouter

from src.api.auth.routes.oauth_authorize import router as oauth_authorize_router
from src.api.auth.routes.oauth_callback import router as oauth_callback_router

router = APIRouter()

router.include_router(oauth_authorize_router)
router.include_router(oauth_callback_router)
