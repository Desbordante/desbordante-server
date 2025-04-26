from fastapi import APIRouter

from src.api.auth.routes.get_access_token import router as get_access_token_router
from src.api.auth.routes.login_user import router as login_user_router
from src.api.auth.routes.logout_user import router as logout_user_router
from src.api.auth.routes.refresh_token import router as refresh_token_router
from src.api.auth.routes.register_user import router as register_user_router

router = APIRouter()

router.include_router(register_user_router)
router.include_router(login_user_router)
router.include_router(logout_user_router)
router.include_router(refresh_token_router)
router.include_router(get_access_token_router)
