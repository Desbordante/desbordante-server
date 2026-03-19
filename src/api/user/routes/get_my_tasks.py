from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.api.dependencies import AuthenticatedActorDep, PaginationParamsDep
from src.api.user.dependencies import GetUserTasksUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResponseSchema
from src.schemas.task_schemas.base_schemas import TaskQueryParamsSchema, TaskSchema

router = APIRouter()

TaskQueryParamsDep = Annotated[TaskQueryParamsSchema, Depends(TaskQueryParamsSchema)]


@router.get(
    "/me/tasks/",
    response_model=PaginatedResponseSchema[TaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Get my tasks",
    description="Get list of current user's tasks",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_my_tasks(
    get_user_tasks: GetUserTasksUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: TaskQueryParamsDep,
    actor: AuthenticatedActorDep,
) -> Any:
    return await get_user_tasks(
        user_id=actor.user_id,
        pagination=pagination,
        query_params=query_params,
    )
