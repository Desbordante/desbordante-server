import sqlalchemy

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.ar.task_result import (
    ArTaskResultFiltersSchema,
    ArTaskResultItemField,
    ArTaskResultOrderingField,
)


class ArQueryHelper(
    BaseQueryHelper[ArTaskResultOrderingField, ArTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: ArTaskResultOrderingField):
        match order_by:
            case ArTaskResultOrderingField.LHS_VALUES:
                return TaskResultModel.result[ArTaskResultItemField.LHS_VALUES].astext
            case ArTaskResultOrderingField.RHS_VALUES:
                return TaskResultModel.result[ArTaskResultItemField.RHS_VALUES].astext
            case ArTaskResultOrderingField.SUPPORT:
                return sqlalchemy.func.cast(
                    TaskResultModel.result[ArTaskResultItemField.SUPPORT],
                    sqlalchemy.Float,
                )
            case ArTaskResultOrderingField.CONFIDENCE:
                return sqlalchemy.func.cast(
                    TaskResultModel.result[ArTaskResultItemField.CONFIDENCE],
                    sqlalchemy.Float,
                )
        super().get_ordering_field(order_by)

    def make_filters(self, filters: ArTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # lhs_values
            TaskResultModel.result[ArTaskResultItemField.LHS_VALUES].op("<@")(
                filters.lhs_values
            )
            if filters.lhs_values
            else None,
            # rhs_values
            TaskResultModel.result[ArTaskResultItemField.RHS_VALUES].op("<@")(
                filters.rhs_values
            )
            if filters.rhs_values
            else None,
            # min_support
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultItemField.SUPPORT],
                sqlalchemy.Float,
            )
            >= filters.min_support
            if filters.min_support is not None
            else None,
            # max_support
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultItemField.SUPPORT],
                sqlalchemy.Float,
            )
            <= filters.max_support
            if filters.max_support is not None
            else None,
            # min_confidence
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultItemField.CONFIDENCE],
                sqlalchemy.Float,
            )
            >= filters.min_confidence
            if filters.min_confidence is not None
            else None,
            # max_confidence
            sqlalchemy.cast(
                TaskResultModel.result[ArTaskResultItemField.CONFIDENCE],
                sqlalchemy.Float,
            )
            <= filters.max_confidence
            if filters.max_confidence is not None
            else None,
        ]
