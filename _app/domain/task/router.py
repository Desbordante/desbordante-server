from typing import List, Union
from uuid import UUID
import json

from fastapi import APIRouter, status, Query

from _app.domain.auth.dependencies.auth import (
    AuthorizedUserDep,
    OptionallyAuthorizedUserDep,
)
from _app.domain.task.dependencies import TaskServiceDep
from _app.domain.task.models import TaskPublic

from _app.exceptions.exceptions import ForbiddenException
from _app.schemas import HTTPApiError

from _app.domain.task.schemas.types import SortOrder
from _app.domain.task.utils import (
    match_filter_by_primitive_name,
    match_sorter_by_primitive_name,
)
from _app.domain.task.schemas.dd.filter import DdFilterOptions
from _app.domain.task.schemas.md.filter import MdFilterOptions
from _app.domain.task.schemas.fd.filter import FdFilterOptions
from _app.domain.task.schemas.afd.filter import AfdFilterOptions
from _app.domain.task.schemas.afd_verification.filter import (
    AfdVerificationFilterOptions,
)
from _app.domain.task.schemas.pfd.filter import PfdFilterOptions
from _app.domain.task.schemas.nar.filter import NarFilterOptions
from _app.domain.task.schemas.ac.filter import AcFilterOptions
from _app.domain.task.schemas.adc.filter import AdcFilterOptions

from _app.domain.task.schemas.dd.sort import DdSortOptions
from _app.domain.task.schemas.md.sort import MdSortOptions
from _app.domain.task.schemas.fd.sort import FdSortOptions
from _app.domain.task.schemas.afd.sort import AfdSortOptions
from _app.domain.task.schemas.afd_verification.sort import AfdVerificationSortOptions
from _app.domain.task.schemas.pfd.sort import PfdSortOptions
from _app.domain.task.schemas.nar.sort import NarSortOptions
from _app.domain.task.schemas.ac.sort import AcSortOptions
from _app.domain.task.schemas.adc.sort import AdcSortOptions


router = APIRouter()

OneOfFilterOption = Union[
    NarFilterOptions,
    DdFilterOptions,
    MdFilterOptions,
    FdFilterOptions,
    PfdFilterOptions,
    AfdFilterOptions,
    AdcFilterOptions,
    AcFilterOptions,
    AfdVerificationFilterOptions,
]

OneOfSortOption = Union[
    FdSortOptions,
    PfdSortOptions,
    AfdSortOptions,
    DdSortOptions,
    NarSortOptions,
    MdSortOptions,
    AcSortOptions,
    AdcSortOptions,
    AfdVerificationSortOptions,
]


# @router.post(
#     "/",
#     response_model=TaskPublic,
#     responses={status.HTTP_403_FORBIDDEN: {"model": HTTPApiError}},
# )
# async def create_task(
#     user: OptionallyAuthorizedUserDep,
#     form_data: TaskCreate,
#     task_service: TaskServiceDep,
#     file_service: FileServiceDep,
# ) -> TaskPublic:
#     initiator_id = user.id if user else None

#     # TODO: Better way to get files
#     files = [file_service.get_file_by_id(file_id) for file_id in form_data.files_ids]

#     for file in files:
#         if file.owner_id is not None and file.owner_id != initiator_id:
#             raise ForbiddenException("Access denied")

#     task = task_service.create_task(
#         config=form_data.config, files=files, initiator_id=initiator_id
#     )
#     return task


@router.get(
    "/{id}",
    response_model=TaskPublic,
    responses={status.HTTP_403_FORBIDDEN: {"model": HTTPApiError}},
)
async def get_task(
    id: UUID,
    user: OptionallyAuthorizedUserDep,
    task_service: TaskServiceDep,
    filter_options: List[OneOfFilterOption] = Query(None),
    filter_params: str = Query(
        None, description="String in JSON format {filter_option: filter_params}"
    ),
    sort_option: OneOfSortOption = Query(None),
    sort_direction: SortOrder = Query(None),
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
        print("filter", filter_options, filter_params)
        filter = json.loads(filter_params)

        filt = match_filter_by_primitive_name(primitive_name)
        for f in filter_options:
            task_result = filt.filter(task_result, f, filter[f])

    if sort_option and sort_direction:
        print("sort", sort_option, sort_direction)
        sorter = match_sorter_by_primitive_name(primitive_name)
        task_result = sorter.sort(task_result, sort_option, sort_direction)

    task.result["result"] = task_result
    return task


@router.get(
    "/",
    response_model=List[TaskPublic],
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPApiError}},
)
async def get_tasks(
    user: AuthorizedUserDep,
    task_service: TaskServiceDep,
) -> List[TaskPublic]:
    return task_service.get_user_tasks(user.id)
