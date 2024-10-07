from fastapi import APIRouter

from internal.rest.http.task.set_task import router as set_task_router
from internal.rest.http.task.retrieve_task import router as retrieve_task_router

router = APIRouter(prefix="/task", tags=["task"])

router.include_router(set_task_router)
router.include_router(retrieve_task_router)
