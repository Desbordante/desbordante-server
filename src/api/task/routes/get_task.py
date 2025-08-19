from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.task.dependencies import GetTaskUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.task_schemas.base_schemas import TaskSchema

router = APIRouter()


@router.get(
    "/{id}/",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
    summary="Get profiling task by id",
    description="Get profiling task by id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_task(
    id: UUID,
    get_task: GetTaskUseCaseDep,
) -> Any:
    return await get_task(id=id)
