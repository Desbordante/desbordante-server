from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.domain.auth.dependencies.auth import (
    AuthorizedUserDep,
    OptionallyAuthorizedUserDep,
)
from app.domain.task.dependencies import TaskServiceDep
from app.domain.task.models import TaskPublic
from app.domain.task.schemas.schemas import TaskCreate
from app.exceptions.exceptions import ForbiddenException

router = APIRouter()


@router.post("/", response_model=TaskPublic)
async def create_task(
    user: OptionallyAuthorizedUserDep,
    config: TaskCreate,
    task_service: TaskServiceDep,
) -> TaskPublic:
    owner_id = user.id if user else None
    print(owner_id)

    task = task_service.create_task(config=config, owner_id=owner_id)
    return task


@router.get("/{id}", response_model=TaskPublic)
async def get_task(
    id: UUID,
    user: OptionallyAuthorizedUserDep,
    task_service: TaskServiceDep,
) -> TaskPublic:
    task = task_service.get_by_id(id)

    user_id = user.id if user else None

    if task.owner_id != user_id:
        raise ForbiddenException("Access denied")

    return task


@router.get("/", response_model=List[TaskPublic])
async def get_tasks(
    user: AuthorizedUserDep,
    task_service: TaskServiceDep,
) -> List[TaskPublic]:
    return task_service.get_user_tasks(user.id)
