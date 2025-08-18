from typing import Any

from fastapi import APIRouter, status

from src.api.dependencies import PaginationParamsDep
from src.api.task.dependencies import GetTasksUseCaseDep, TaskQueryParamsDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResponseSchema
from src.schemas.task_schemas.base_schemas import TaskSchema

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponseSchema[TaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Get profiling tasks",
    description="Get profiling tasks",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_tasks(
    pagination: PaginationParamsDep,
    get_tasks: GetTasksUseCaseDep,
    query_params: TaskQueryParamsDep,
) -> Any:
    return await get_tasks(
        pagination=pagination,
        query_params=query_params,
    )
