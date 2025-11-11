from fastapi import APIRouter

from src.api.account.routes.get_info import router as get_info_router
from src.api.account.routes.get_stats import router as get_stats_router

router = APIRouter()

router.include_router(get_info_router)
router.include_router(get_stats_router)
