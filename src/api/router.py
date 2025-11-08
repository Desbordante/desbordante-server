from fastapi import APIRouter

from src.api.account import router as account_router
from src.api.common import router as common_router
from src.api.dataset import router as dataset_router
from src.api.old import router as old_router

router = APIRouter(prefix="/v1")

router.include_router(common_router, tags=["common"])
router.include_router(old_router, prefix="/old", tags=["old"])
router.include_router(account_router, prefix="/account", tags=["account"])
router.include_router(dataset_router, prefix="/datasets", tags=["dataset"])
