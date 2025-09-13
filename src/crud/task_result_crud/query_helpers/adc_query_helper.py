from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import JSONB

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultFiltersSchema,
    AdcTaskResultItemField,
    AdcTaskResultOrderingField,
)


class AdcQueryHelper(
    BaseQueryHelper[AdcTaskResultOrderingField, AdcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AdcTaskResultOrderingField):
        match order_by:
            case AdcTaskResultOrderingField.LhsColumns:
                return TaskResultModel.result[AdcTaskResultItemField.LhsColumns].astext
            case AdcTaskResultOrderingField.RhsColumns:
                return TaskResultModel.result[AdcTaskResultItemField.RhsColumns].astext
            case AdcTaskResultOrderingField.LhsIndices:
                return TaskResultModel.result[AdcTaskResultItemField.LhsIndices].astext
            case AdcTaskResultOrderingField.RhsIndices:
                return TaskResultModel.result[AdcTaskResultItemField.RhsIndices].astext
            case AdcTaskResultOrderingField.NumberOfConjuncts:
                return func.jsonb_array_length(
                    TaskResultModel.result[AdcTaskResultItemField.Cojuncts]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AdcTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result[AdcTaskResultItemField.Cojuncts].astext.icontains(
                filters.search
            )
            if filters.search
            else None,
            # lhs_columns
            TaskResultModel.result[AdcTaskResultItemField.LhsColumns].op("<@")(
                cast(filters.lhs_columns, JSONB)
            )
            if filters.lhs_columns
            else None,
            # rhs_columns
            TaskResultModel.result[AdcTaskResultItemField.RhsColumns].op("<@")(
                cast(filters.rhs_columns, JSONB)
            )
            if filters.rhs_columns
            else None,
            # lhs_indices
            TaskResultModel.result[AdcTaskResultItemField.LhsIndices].op("<@")(
                cast(filters.lhs_indices, JSONB)
            )
            if filters.lhs_indices
            else None,
            # rhs_indices
            TaskResultModel.result[AdcTaskResultItemField.RhsIndices].op("<@")(
                cast(filters.rhs_indices, JSONB)
            )
            if filters.rhs_indices
            else None,
        ]
