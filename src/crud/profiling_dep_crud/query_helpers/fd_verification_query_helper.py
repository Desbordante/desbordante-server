import sqlalchemy as sa
from sqlalchemy import func

from src.crud.profiling_dep_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_models import ProfilingDepModel
from src.schemas.task_schemas.primitives.fd_verification.task_result import (
    FdVerificationTaskResultFiltersSchema,
    FdVerificationTaskResultItemField,
    FdVerificationTaskResultOrderingField,
)


class FdVerificationQueryHelper(
    BaseQueryHelper[
        FdVerificationTaskResultOrderingField, FdVerificationTaskResultFiltersSchema
    ]
):
    def get_ordering_field(self, order_by: FdVerificationTaskResultOrderingField):
        match order_by:
            case FdVerificationTaskResultOrderingField.NUMBER_OF_DISTINCT_RHS_VALUES:
                return func.cast(
                    ProfilingDepModel.result[
                        FdVerificationTaskResultItemField.NUMBER_OF_DISTINCT_RHS_VALUES
                    ],
                    sa.Integer,
                )
            case (
                FdVerificationTaskResultOrderingField.MOST_FREQUENT_RHS_VALUE_PROPORTION
            ):
                return func.cast(
                    ProfilingDepModel.result[
                        FdVerificationTaskResultItemField.MOST_FREQUENT_RHS_VALUE_PROPORTION
                    ],
                    sa.Float,
                )
            case FdVerificationTaskResultOrderingField.NUMBER_OF_ROWS:
                return func.jsonb_array_length(
                    ProfilingDepModel.result[FdVerificationTaskResultItemField.ROWS]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: FdVerificationTaskResultFiltersSchema):
        return [
            # search
            ProfilingDepModel.result[
                FdVerificationTaskResultItemField.ROWS
            ].astext.icontains(filters.search)
            if filters.search
            else None,
            # min_number_of_distinct_rhs_values
            func.cast(
                ProfilingDepModel.result[
                    FdVerificationTaskResultItemField.NUMBER_OF_DISTINCT_RHS_VALUES
                ],
                sa.Integer,
            )
            >= filters.min_num
            if filters.min_num is not None
            else None,
            # max_number_of_distinct_rhs_values
            func.cast(
                ProfilingDepModel.result[
                    FdVerificationTaskResultItemField.NUMBER_OF_DISTINCT_RHS_VALUES
                ],
                sa.Integer,
            )
            <= filters.max_num
            if filters.max_num is not None
            else None,
            # min_most_frequent_rhs_value_proportion
            func.cast(
                ProfilingDepModel.result[
                    FdVerificationTaskResultItemField.MOST_FREQUENT_RHS_VALUE_PROPORTION
                ],
                sa.Float,
            )
            >= filters.min_prop
            if filters.min_prop is not None
            else None,
            # max_most_frequent_rhs_value_proportion
            func.cast(
                ProfilingDepModel.result[
                    FdVerificationTaskResultItemField.MOST_FREQUENT_RHS_VALUE_PROPORTION
                ],
                sa.Float,
            )
            <= filters.max_prop
            if filters.max_prop is not None
            else None,
        ]
