from fastapi import APIRouter

from .auth import router as auth_router
from .common import router as common_router

router = APIRouter()

router.include_router(common_router, prefix="", tags=["common"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
