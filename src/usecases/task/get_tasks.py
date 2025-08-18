from typing import Protocol

from src.models.task_models import TaskModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import TaskQueryParamsSchema


class TaskCrud(Protocol):
    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskQueryParamsSchema,
        owner_id: int,
    ) -> PaginatedResult[TaskModel]: ...


class GetTasksUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        user: UserModel,
    ):
        self.task_crud = task_crud
        self.user = user

    async def __call__(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskQueryParamsSchema,
    ) -> PaginatedResult[TaskModel]:
        return await self.task_crud.get_many(
            pagination=pagination,
            query_params=query_params,
            owner_id=self.user.id,
        )
