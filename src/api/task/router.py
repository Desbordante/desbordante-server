from fastapi import APIRouter

from src.api.task.routes.get_task import router as get_task_router

router = APIRouter()

router.include_router(get_task_router)
