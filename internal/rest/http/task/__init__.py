from fastapi import APIRouter

from internal.rest.http.task.set_task import router as set_task_router

router = APIRouter(prefix="/task", tags=["task"])

router.include_router(set_task_router)
