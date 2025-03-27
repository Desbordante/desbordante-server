from typing import List
from uuid import UUID

from fastapi import APIRouter

from app.domain.auth.dependencies.auth import (
    AuthorizedUserDep,
    OptionallyAuthorizedUserDep,
)
from app.domain.file.dependencies import FileServiceDep
from app.domain.task.dependencies import TaskServiceDep
from app.domain.task.models import TaskPublic
from app.domain.task.schemas.schemas import TaskCreate
from app.exceptions.exceptions import ForbiddenException

router = APIRouter()


@router.post("/", response_model=TaskPublic)
async def create_task(
    user: OptionallyAuthorizedUserDep,
    form_data: TaskCreate,
    task_service: TaskServiceDep,
    file_service: FileServiceDep,
) -> TaskPublic:
    initiator_id = user.id if user else None

    # TODO: Better way to get files
    files = [file_service.get_file_by_id(file_id) for file_id in form_data.files_ids]

    for file in files:
        if file.owner_id is not None and file.owner_id != initiator_id:
            raise ForbiddenException("Access denied")

    task = task_service.create_task(
        config=form_data.config, files=files, initiator_id=initiator_id
    )
    return task


@router.get("/{id}", response_model=TaskPublic)
async def get_task(
    id: UUID,
    user: OptionallyAuthorizedUserDep,
    task_service: TaskServiceDep,
) -> TaskPublic:
    task = task_service.get_by_id(id)

    user_id = user.id if user else None

    if task.initiator_id != user_id:
        raise ForbiddenException("Access denied")

    return task


@router.get("/", response_model=List[TaskPublic])
async def get_tasks(
    user: AuthorizedUserDep,
    task_service: TaskServiceDep,
) -> List[TaskPublic]:
    return task_service.get_user_tasks(user.id)
