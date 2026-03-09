from typing import Sequence, TypedDict, Unpack
from uuid import UUID

from sqlalchemy import ColumnElement, ColumnExpressionArgument, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Bundle

from src.crud.base_crud import BaseCrud
from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.crud.task_result_crud.utils import get_query_helper_by_primitive_name
from src.models.task_result_models import TaskResultModel
from src.schemas.base_schemas import (
    FiltersParamsSchema,
    PaginatedResult,
    PaginationParamsSchema,
)
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
    _query_helper: BaseQueryHelper

    def __init__(self, *, session: AsyncSession, primitive_name: PrimitiveName):
        self._query_helper = get_query_helper_by_primitive_name(primitive_name)

        super().__init__(session=session)

    async def get_by(self, **kwargs: Unpack[TaskResultFindProps]) -> TaskResultModel:
        return await super().get_by(**kwargs)

    def _get_ordering_field(self, order_by: str) -> ColumnElement[TaskResultModel]:
        return self._query_helper.get_ordering_field(order_by)

    def _make_filters(
        self, filters_params: FiltersParamsSchema
    ) -> Sequence[ColumnExpressionArgument[bool] | None]:
        return self._query_helper.make_filters(filters_params)

    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: TaskResultQueryParamsSchema,
        **kwargs: Unpack[TaskResultFindProps],
    ) -> PaginatedResult[TaskResultModel]:
        filtered_result_column = self._query_helper.get_filtered_result_column(
            query_params.filters
        )

        if filtered_result_column is None:
            return await super()._get_many(
                pagination=pagination,
                query_params=query_params,
                query=select(TaskResultModel),
                **kwargs,
            )

        cte = (
            select(
                TaskResultModel.id,
                filtered_result_column.label("result"),
                TaskResultModel.task_id,
                TaskResultModel.created_at,
                TaskResultModel.updated_at,
            )
            .filter_by(**kwargs)
            .cte("filtered_results")
        )

        query = select(
            Bundle(
                "TaskResultModel",
                cte.c.id,
                cte.c.result,
                cte.c.task_id,
                cte.c.created_at,
                cte.c.updated_at,
            )
        )

        return await super()._get_many(
            pagination=pagination,
            query_params=query_params,
            query=query,
            **kwargs,
        )

    async def update(
        self, *, entity: TaskResultModel, **kwargs: Unpack[TaskResultUpdateProps]
    ) -> TaskResultModel:
        return await super().update(entity=entity, **kwargs)
