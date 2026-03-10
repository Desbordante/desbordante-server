from typing import Protocol
from uuid import UUID

from src.models.task_result_models import TaskResultModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema


class TaskResultCrud(Protocol):
    async def get_by(self, *, task_id: UUID) -> TaskResultModel: ...
    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
        task_id: UUID,
    ) -> PaginatedResult[TaskResultModel]: ...


class GetTaskResultsUseCase:
    def __init__(
        self,
        *,
        task_result_crud: TaskResultCrud,
    ):
        self.task_result_crud = task_result_crud

    async def __call__(
        self,
        *,
        task_id: UUID,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
    ) -> PaginatedResult[TaskResultModel]:
        return await self.task_result_crud.get_many(
            pagination=pagination,
            query_params=query_params,
            task_id=task_id,
        )
