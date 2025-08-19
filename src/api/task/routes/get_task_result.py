from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.task.dependencies import GetTaskResultUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.task_schemas.base_schemas import TaskResultSchema

router = APIRouter()


@router.get(
    "/{id}/result/",
    response_model=TaskResultSchema,
    status_code=status.HTTP_200_OK,
    summary="Get profiling task result by task id",
    description="Get profiling task result by task id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_task_result(
    id: UUID,
    get_task_result: GetTaskResultUseCaseDep,
) -> Any:
    return await get_task_result(task_id=id)
