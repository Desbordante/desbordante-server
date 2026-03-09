from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.api.dependencies import PaginationParamsDep, get_admin_actor
from src.api.user.dependencies import GetUserTasksUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResult
from src.schemas.task_schemas.base_schemas import TaskQueryParamsSchema, TaskSchema

router = APIRouter()

TaskQueryParamsDep = Annotated[TaskQueryParamsSchema, Depends(TaskQueryParamsSchema)]


@router.get(
    "/{user_id}/tasks/",
    response_model=PaginatedResult[TaskSchema],
    status_code=status.HTTP_200_OK,
    summary="Get user's tasks (admin only)",
    description="Get list of specific user's tasks (admin only)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
    },
    dependencies=[Depends(get_admin_actor)],
)
async def get_user_tasks(
    user_id: int,
    get_user_tasks: GetUserTasksUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: TaskQueryParamsDep,
) -> Any:
    return await get_user_tasks(
        user_id=user_id,
        pagination=pagination,
        query_params=query_params,
    )
