from fastapi import APIRouter

from src.api.user.routes.get_me import router as get_me_router
from src.api.user.routes.get_my_stats import router as get_my_stats_router
from src.api.user.routes.get_user_by_id import router as get_user_by_id_router
from src.api.user.routes.get_user_stats import router as get_user_stats_router

router = APIRouter()


router.include_router(get_me_router)
router.include_router(get_my_stats_router)
router.include_router(get_user_by_id_router)
router.include_router(get_user_stats_router)
