from typing import Protocol
from uuid import UUID

from src.models.task_models import ProfilingDepModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import TaskResultQueryParamsSchema


class TaskResultCrud(Protocol):
    async def get_by(self, *, task_id: UUID) -> ProfilingDepModel: ...
    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
        task_id: UUID,
    ) -> PaginatedResult[ProfilingDepModel]: ...


class GetTaskResultsUseCase:
    def __init__(
        self,
        *,
        profiling_dep_crud: TaskResultCrud,
    ):
        self.profiling_dep_crud = profiling_dep_crud

    async def __call__(
        self,
        *,
        task_id: UUID,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
    ) -> PaginatedResult[ProfilingDepModel]:
        return await self.profiling_dep_crud.get_many(
            pagination=pagination,
            query_params=query_params,
            task_id=task_id,
        )
