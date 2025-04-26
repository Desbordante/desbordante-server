from fastapi import APIRouter

from .auth import router as auth_router
from .common import router as common_router
from .file import router as file_router

# from .task import router as task_router
from .user import router as user_router

router = APIRouter()

router.include_router(common_router, prefix="", tags=["common"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(user_router, prefix="/users", tags=["user"])
router.include_router(file_router, prefix="", tags=[])
# router.include_router(task_router, prefix="/tasks", tags=["task"])
