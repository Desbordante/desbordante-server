from fastapi import APIRouter

from src.api.account import router as account_router
from src.api.auth import router as auth_router
from src.api.common import router as common_router

router = APIRouter()

router.include_router(common_router, tags=["common"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(account_router, prefix="/account", tags=["account"])
