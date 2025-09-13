import sqlalchemy as sa
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.afd_verification.task_result import (
    AfdVerificationTaskResultFiltersSchema,
    AfdVerificationTaskResultItemField,
    AfdVerificationTaskResultOrderingField,
)


class AfdVerificationQueryHelper(
    BaseQueryHelper[
        AfdVerificationTaskResultOrderingField, AfdVerificationTaskResultFiltersSchema
    ]
):
    def get_ordering_field(self, order_by: AfdVerificationTaskResultOrderingField):
        match order_by:
            case AfdVerificationTaskResultOrderingField.NumberOfDistinctRhsValues:
                return func.cast(
                    TaskResultModel.result[
                        AfdVerificationTaskResultItemField.NumberOfDistinctRhsValues
                    ],
                    sa.Integer,
                )
            case AfdVerificationTaskResultOrderingField.MostFrequentRhsValueProportion:
                return func.cast(
                    TaskResultModel.result[
                        AfdVerificationTaskResultItemField.MostFrequentRhsValueProportion
                    ],
                    sa.Float,
                )
            case AfdVerificationTaskResultOrderingField.NumberOfRows:
                return func.jsonb_array_length(
                    TaskResultModel.result[AfdVerificationTaskResultItemField.Rows]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AfdVerificationTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # min_number_of_distinct_rhs_values
            func.cast(
                TaskResultModel.result[
                    AfdVerificationTaskResultItemField.NumberOfDistinctRhsValues
                ],
                sa.Integer,
            )
            >= filters.min_num
            if filters.min_num is not None
            else None,
            # max_number_of_distinct_rhs_values
            func.cast(
                TaskResultModel.result[
                    AfdVerificationTaskResultItemField.NumberOfDistinctRhsValues
                ],
                sa.Integer,
            )
            <= filters.max_num
            if filters.max_num is not None
            else None,
            # min_most_frequent_rhs_value_proportion
            func.cast(
                TaskResultModel.result[
                    AfdVerificationTaskResultItemField.MostFrequentRhsValueProportion
                ],
                sa.Float,
            )
            >= filters.min_prop
            if filters.min_prop is not None
            else None,
            # max_most_frequent_rhs_value_proportion
            func.cast(
                TaskResultModel.result[
                    AfdVerificationTaskResultItemField.MostFrequentRhsValueProportion
                ],
                sa.Float,
            )
            <= filters.max_prop
            if filters.max_prop is not None
            else None,
        ]
