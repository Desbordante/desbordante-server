from typing import Any

from fastapi import APIRouter, status

from src.api.task.dependencies import CreateTaskUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.task_schemas.base_schemas import OneOfTaskParams, TaskSchema

router = APIRouter()


@router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create profiling task",
    description="Create profiling task",
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema}},
)
async def create_task(
    create_task: CreateTaskUseCaseDep,
    params: OneOfTaskParams,
) -> Any:
    return await create_task(params=params)
