from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.common import router as common_router
from src.api.dataset import router as dataset_router
from src.api.user import router as user_router

router = APIRouter(prefix="/v1")

router.include_router(common_router, tags=["common"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/users", tags=["user"])
router.include_router(dataset_router, prefix="/datasets", tags=["dataset"])
