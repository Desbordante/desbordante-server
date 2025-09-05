import sqlalchemy

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.ar.task_result import (
    ArTaskResultFiltersSchema,
    ArTaskResultOrderingField,
)


class ArQueryHelper(
    BaseQueryHelper[ArTaskResultOrderingField, ArTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: ArTaskResultOrderingField):
        match order_by:
            case ArTaskResultOrderingField.Left:
                return TaskResultModel.result[order_by].astext
            case ArTaskResultOrderingField.Right:
                return TaskResultModel.result[order_by].astext
            case ArTaskResultOrderingField.Support:
                return sqlalchemy.func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Float
                )
            case ArTaskResultOrderingField.Confidence:
                return sqlalchemy.func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Float
                )
        super().get_ordering_field(order_by)

    def make_filters(self, filters: ArTaskResultFiltersSchema):
        return [
            # search
            sqlalchemy.or_(
                TaskResultModel.result[ArTaskResultOrderingField.Left].astext.icontains(
                    filters.search
                ),
                TaskResultModel.result[
                    ArTaskResultOrderingField.Right
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # left
            TaskResultModel.result[ArTaskResultOrderingField.Left].op("@>")(
                filters.left
            )
            if filters.left
            else None,
            # right
            TaskResultModel.result[ArTaskResultOrderingField.Right].op("@>")(
                filters.right
            )
            if filters.right
            else None,
            # min support
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultOrderingField.Support],
                sqlalchemy.Float,
            )
            >= filters.min_support
            if filters.min_support is not None
            else None,
            # max support
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultOrderingField.Support],
                sqlalchemy.Float,
            )
            <= filters.max_support
            if filters.max_support is not None
            else None,
            # min confidence
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultOrderingField.Confidence],
                sqlalchemy.Float,
            )
            >= filters.min_confidence
            if filters.min_confidence is not None
            else None,
            # max confidence
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultOrderingField.Confidence],
                sqlalchemy.Float,
            )
            <= filters.max_confidence
            if filters.max_confidence is not None
            else None,
        ]
