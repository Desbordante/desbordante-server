from fastapi import APIRouter

from src.api.task.routes.create_task import router as create_task_router

router = APIRouter()

router.include_router(create_task_router)
