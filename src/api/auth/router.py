from fastapi import APIRouter

from src.api.auth.routes import logout, oauth_authorize, oauth_callback

router = APIRouter()

router.include_router(oauth_authorize.router)
router.include_router(oauth_callback.router)
router.include_router(logout.router)
