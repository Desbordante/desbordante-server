from typing import List
from fastapi import Query
from uuid import UUID
import json

from fastapi import APIRouter

from app.domain.auth.dependencies.auth import (
    AuthorizedUserDep,
    OptionallyAuthorizedUserDep,
)
from app.domain.file.dependencies import FileServiceDep
from app.domain.task.dependencies import TaskServiceDep
from app.domain.task.models import TaskPublic
from app.domain.task.utils import (
    match_filter_by_primitive_name,
    match_sorter_by_primitive_name,
)
from app.domain.task.schemas.schemas import TaskCreate
from app.domain.task.schemas.types import SortOrder
from app.exceptions.exceptions import ForbiddenException

from app.domain.task.schemas.schemas import OneOfFilterOption, OneOfSortOption


router = APIRouter()


@router.post("", response_model=TaskPublic)
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
    filter_options: List[OneOfFilterOption] = Query(None),
    filter_params: str = Query(
        None, description="String in JSON format {filter_option: filter_param}"
    ),
    sort_option: OneOfSortOption = Query(None),
    sort_direction: SortOrder = Query(None),
    pagination_offset: int = Query(0),
    pagination_limit: int = Query(0),
) -> TaskPublic:
    task = task_service.get_by_id(id)
    user_id = user.id if user else None

    if task.initiator_id != user_id:
        raise ForbiddenException("Access denied")

    if task.result is None:
        return task

    task_result = task.result["result"]
    primitive_name = task.result["primitive_name"]

    if filter_options and filter_params:
        filter = json.loads(filter_params)

        filt = match_filter_by_primitive_name(primitive_name)
        for f in filter_options:
            task_result = filt.filter(task_result, f, filter[f])

    if sort_option and sort_direction:
        sorter = match_sorter_by_primitive_name(primitive_name)
        task_result = sorter.sort(task_result, sort_option, sort_direction)

    if pagination_limit > 0:
        task.result["count_results"] = len(task_result)
        task_result = task_result[
            pagination_offset : pagination_offset + pagination_limit
        ]

    task.result["result"] = task_result
    return task


@router.get("", response_model=List[TaskPublic])
async def get_tasks(
    user: AuthorizedUserDep,
    task_service: TaskServiceDep,
) -> List[TaskPublic]:
    return task_service.get_user_tasks(user.id)
