from fastapi import APIRouter

from src.api.account.routes.change_password import router as change_password_router
from src.api.account.routes.confirm_email import router as confirm_email_router
from src.api.account.routes.get_me import router as get_me_router
from src.api.account.routes.send_confirmation_email import (
    router as send_verification_email_router,
)

router = APIRouter()

router.include_router(get_me_router)
router.include_router(send_verification_email_router)
router.include_router(confirm_email_router)
router.include_router(change_password_router)
