from typing import Protocol

from src.models.task_models import ProfilingTaskModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import TaskQueryParamsSchema


class TaskCrud(Protocol):
    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskQueryParamsSchema,
        owner_id: int,
    ) -> PaginatedResult[ProfilingTaskModel]: ...


class GetUserTasksUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
    ):
        self._task_crud = task_crud

    async def __call__(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskQueryParamsSchema,
        user_id: int,
    ) -> PaginatedResult[ProfilingTaskModel]:
        return await self._task_crud.get_many(
            pagination=pagination,
            query_params=query_params,
            owner_id=user_id,
        )
