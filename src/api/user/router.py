from fastapi import APIRouter

from src.api.user.routes.get_current_user import router as get_current_user_router

router = APIRouter()

router.include_router(get_current_user_router)
