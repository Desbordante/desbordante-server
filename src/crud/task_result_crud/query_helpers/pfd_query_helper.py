from sqlalchemy import func, or_

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.pfd.task_result import (
    PfdTaskResultFiltersSchema,
    PfdTaskResultOrderingField,
)


class PfdQueryHelper(
    BaseQueryHelper[PfdTaskResultOrderingField, PfdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: PfdTaskResultOrderingField):
        match order_by:
            case PfdTaskResultOrderingField.NumberOfLhs:
                return func.jsonb_array_length(PfdTaskResultOrderingField.Lhs)
            case PfdTaskResultOrderingField.NumberOfRhs:
                return func.jsonb_array_length(PfdTaskResultOrderingField.Rhs)
            case PfdTaskResultOrderingField.Lhs:
                return TaskResultModel.result[order_by].astext
            case PfdTaskResultOrderingField.Rhs:
                return TaskResultModel.result[order_by].astext

        super().get_ordering_field(order_by)

    def make_filters(self, filters: PfdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[PfdTaskResultOrderingField.Lhs].astext.icontains(
                    filters.search
                ),
                TaskResultModel.result[PfdTaskResultOrderingField.Rhs].astext.icontains(
                    filters.search
                ),
            )
            if filters.search
            else None,
        ]
