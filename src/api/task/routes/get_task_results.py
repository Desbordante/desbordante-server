from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dependencies import PaginationParamsDep
from src.api.task.dependencies import GetTaskResultsUseCaseDep, TaskResultQueryParamsDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResponseSchema
from src.schemas.task_schemas.base_schemas import OneOfTaskResult

router = APIRouter()


@router.get(
    "/{id}/results/",
    response_model=PaginatedResponseSchema[OneOfTaskResult],
    status_code=status.HTTP_200_OK,
    summary="Get profiling task results by task id",
    description="Get profiling task results by task id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_task_results(
    id: UUID,
    get_task_results: GetTaskResultsUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: TaskResultQueryParamsDep,
) -> Any:
    results = await get_task_results(
        task_id=id,
        pagination=pagination,
        query_params=query_params,
    )

    return PaginatedResponseSchema(
        items=[r.result for r in results.items],
        total_count=results.total_count,
        limit=results.limit,
        offset=results.offset,
    )
