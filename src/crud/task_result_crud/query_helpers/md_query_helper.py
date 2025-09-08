from sqlalchemy import func, or_

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.md.task_result import (
    MdTaskResultFiltersSchema,
    MdTaskResultOrderingField,
)


class MdQueryHelper(
    BaseQueryHelper[MdTaskResultOrderingField, MdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: MdTaskResultOrderingField):
        match order_by:
            case MdTaskResultOrderingField.NumberOfLhs:
                return func.jsonb_array_length(MdTaskResultOrderingField.Lhs)
            case MdTaskResultOrderingField.NumberOfRhs:
                return func.jsonb_array_length(MdTaskResultOrderingField.Rhs)
            case MdTaskResultOrderingField.Lhs:
                return TaskResultModel.result[order_by].astext
            case MdTaskResultOrderingField.Rhs:
                return TaskResultModel.result[order_by].astext

        super().get_ordering_field(order_by)

    def make_filters(self, filters: MdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[MdTaskResultOrderingField.Lhs].astext.icontains(
                    filters.search
                ),
                TaskResultModel.result[MdTaskResultOrderingField.Rhs].astext.icontains(
                    filters.search
                ),
            )
            if filters.search
            else None,
            # metrics
            func.exists(
                func.jsonb_array_elements(
                    TaskResultModel.result[MdTaskResultOrderingField.Lhs]
                )["metrics"].op("?|")(filters.metrics)
            )
            if filters.metrics
            else None,
            # show zeroes
            func.exists(
                func.jsonb_array_elements(
                    TaskResultModel.result[MdTaskResultOrderingField.Lhs]
                )["boundary"].op(">")(0)
            )
            if not filters.show_zeroes
            else None,
        ]
