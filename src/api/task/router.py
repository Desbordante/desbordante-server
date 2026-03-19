from fastapi import APIRouter

from src.api.task.routes.create_task import router as create_task_router
from src.api.task.routes.get_task import router as get_task_router
from src.api.task.routes.get_task_results import router as get_task_result_router
from src.api.task.routes.get_tasks import router as get_tasks_router

router = APIRouter()

router.include_router(create_task_router)
router.include_router(get_tasks_router)
router.include_router(get_task_router)
router.include_router(get_task_result_router)
