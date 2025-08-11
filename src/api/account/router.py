from fastapi import APIRouter

from src.api.account.routes.change_password import router as change_password_router
from src.api.account.routes.confirm_email import router as confirm_email_router
from src.api.account.routes.get_info import router as get_info_router
from src.api.account.routes.get_stats import router as get_stats_router
from src.api.account.routes.send_confirmation_email import (
    router as send_verification_email_router,
)
from src.api.account.routes.update_info import router as update_info_router

router = APIRouter()

router.include_router(get_info_router)
router.include_router(get_stats_router)
router.include_router(update_info_router)
router.include_router(change_password_router)
router.include_router(send_verification_email_router)
router.include_router(confirm_email_router)
