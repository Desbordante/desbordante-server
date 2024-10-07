from fastapi import APIRouter

from internal.rest.http.common import router as common_router
from internal.rest.http.file import router as file_router
from internal.rest.http.user import router as user_router
from internal.rest.http.task import router as task_router

router = APIRouter(prefix="/api")

router.include_router(common_router)
router.include_router(file_router)
router.include_router(user_router)
router.include_router(task_router)
