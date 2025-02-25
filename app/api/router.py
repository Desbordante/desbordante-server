from fastapi import APIRouter

from .common import router as common_router

router = APIRouter()

router.include_router(common_router, prefix="", tags=["common"])
