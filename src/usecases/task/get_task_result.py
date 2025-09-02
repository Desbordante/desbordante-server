from typing import Protocol
from uuid import UUID

from src.models.task_models import TaskResultModel
from src.models.user_models import UserModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskResult,
    TaskResultQueryParamsSchema,
)


class TaskResultCrud(Protocol):
    async def get_by(self, *, task_id: UUID) -> TaskResultModel: ...
    async def get_results(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
        task_id: UUID,
    ) -> PaginatedResult[OneOfTaskResult]: ...


class GetTaskResultUseCase:
    def __init__(
        self,
        *,
        task_result_crud: TaskResultCrud,
        user: UserModel,
    ):
        self.task_result_crud = task_result_crud
        self.user = user

    async def __call__(
        self,
        *,
        task_id: UUID,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
    ) -> PaginatedResult[OneOfTaskResult]:
        return await self.task_result_crud.get_results(
            pagination=pagination,
            query_params=query_params,
            task_id=task_id,
        )
