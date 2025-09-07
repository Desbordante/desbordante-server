import sqlalchemy
from sqlalchemy import func, or_

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.nar.task_result import (
    NarTaskResultFiltersSchema,
    NarTaskResultOrderingField,
)


class NarQueryHelper(
    BaseQueryHelper[NarTaskResultOrderingField, NarTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: NarTaskResultOrderingField):
        match order_by:
            case NarTaskResultOrderingField.NumberOfLhs:
                return func.jsonb_array_length(NarTaskResultOrderingField.Lhs)
            case NarTaskResultOrderingField.NumberOfRhs:
                return func.jsonb_array_length(NarTaskResultOrderingField.Rhs)
            case NarTaskResultOrderingField.Lhs:
                return TaskResultModel.result[order_by].astext
            case NarTaskResultOrderingField.Rhs:
                return TaskResultModel.result[order_by].astext
            case NarTaskResultOrderingField.Confidence:
                return func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Float
                )
            case NarTaskResultOrderingField.Support:
                return sqlalchemy.func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Float
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: NarTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[NarTaskResultOrderingField.Lhs].astext.icontains(
                    filters.search
                ),
                TaskResultModel.result[NarTaskResultOrderingField.Rhs].astext.icontains(
                    filters.search
                ),
            )
            if filters.search
            else None,
        ]
