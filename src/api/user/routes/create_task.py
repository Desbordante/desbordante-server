from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dependencies import ActorDep
from src.api.user.dependencies import CreateTaskUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.task_schemas import OneOfTaskConfig, TaskSchema

router = APIRouter()


@router.post(
    "/me/tasks/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create private profiling task",
    description="Create private profiling task",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def create_task(
    dataset_id: UUID,
    config: OneOfTaskConfig,
    create_task: CreateTaskUseCaseDep,
    actor: ActorDep,
) -> Any:
    return await create_task(actor=actor, dataset_id=dataset_id, config=config)
