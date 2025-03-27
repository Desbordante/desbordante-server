from uuid import UUID

from fastapi import APIRouter

from app.domain.task.dependencies import TaskServiceDep
from app.domain.task.models import TaskPublic
from app.domain.task.schemas.schemas import TaskCreate

router = APIRouter()


@router.post("/", response_model=TaskPublic)
async def create_task(
    config: TaskCreate,
    task_service: TaskServiceDep,
) -> TaskPublic:
    task = task_service.create_task(config)
    return task


@router.get("/{id}", response_model=TaskPublic)
async def get_task(
    id: UUID,
    task_service: TaskServiceDep,
) -> TaskPublic:
    task = task_service.get_by_id(id)
    return task
