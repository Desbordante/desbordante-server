from typing import TypedDict, Unpack
from uuid import UUID

from src.crud.base_crud import BaseCrud
from src.models.task_models import TaskResultModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskResult,
    TaskResultQueryParamsSchema,
)


class TaskResultFindProps(TypedDict, total=False):
    id: UUID
    task_id: UUID


class TaskResultUpdateProps(TypedDict, total=False):
    pass


class TaskResultCrud(BaseCrud[TaskResultModel, UUID]):
    model = TaskResultModel

    async def get_by(self, **kwargs: Unpack[TaskResultFindProps]) -> TaskResultModel:
        return await super().get_by(**kwargs)

    async def get_results(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
        **kwargs: Unpack[TaskResultFindProps],
    ) -> PaginatedResult[OneOfTaskResult]:
        return PaginatedResult(
            items=[],
            total_count=0,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def update(
        self, *, entity: TaskResultModel, **kwargs: Unpack[TaskResultUpdateProps]
    ) -> TaskResultModel:
        return await super().update(entity=entity, **kwargs)
