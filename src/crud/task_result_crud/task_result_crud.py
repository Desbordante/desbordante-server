from typing import Any, TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.crud.task_result_crud.utils import get_query_helper_by_primitive_name
from src.models.task_result_models import TaskResultModel
from src.schemas.base_schemas import PaginatedResult, PaginationParamsSchema
from src.schemas.task_schemas.base_schemas import (
    TaskResultQueryParamsSchema,
)
from src.schemas.task_schemas.types import PrimitiveName


class TaskResultFindProps(TypedDict, total=False):
    id: UUID
    task_id: UUID


class TaskResultUpdateProps(TypedDict, total=False):
    pass


class TaskResultCrud(BaseCrud[TaskResultModel, UUID]):
    model = TaskResultModel
    _query_helper: BaseQueryHelper[Any]

    def __init__(self, *, session: AsyncSession, primitive_name: PrimitiveName):
        self._query_helper = get_query_helper_by_primitive_name(primitive_name)

        super().__init__(session=session)

    async def get_by(self, **kwargs: Unpack[TaskResultFindProps]) -> TaskResultModel:
        return await super().get_by(**kwargs)

    def _get_ordering_field(self, order_by: str) -> ColumnElement[TaskResultModel]:
        return self._query_helper.get_ordering_field(order_by)

    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
        **kwargs: Unpack[TaskResultFindProps],
    ) -> PaginatedResult[TaskResultModel]:
        return await super().get_many(
            pagination=pagination,
            query_params=query_params,
            **kwargs,
        )

    async def update(
        self, *, entity: TaskResultModel, **kwargs: Unpack[TaskResultUpdateProps]
    ) -> TaskResultModel:
        return await super().update(entity=entity, **kwargs)
