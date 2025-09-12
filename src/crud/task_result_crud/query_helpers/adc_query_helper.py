from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import JSONB

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultField,
    AdcTaskResultFiltersSchema,
    AdcTaskResultOrderingField,
)


class AdcQueryHelper(
    BaseQueryHelper[AdcTaskResultOrderingField, AdcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AdcTaskResultOrderingField):
        match order_by:
            case AdcTaskResultOrderingField.LeftColumns:
                return TaskResultModel.result[AdcTaskResultField.LeftColumns].astext
            case AdcTaskResultOrderingField.RightColumns:
                return TaskResultModel.result[AdcTaskResultField.RightColumns].astext
            case AdcTaskResultOrderingField.NumberOfConjuncts:
                return func.jsonb_array_length(
                    TaskResultModel.result[AdcTaskResultField.Cojuncts]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AdcTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result[AdcTaskResultField.Cojuncts].astext.icontains(
                filters.search
            )
            if filters.search
            else None,
            # left_columns
            TaskResultModel.result[AdcTaskResultField.LeftColumns].op("<@")(
                cast(filters.left_columns, JSONB)
            )
            if filters.left_columns
            else None,
            # right_columns
            TaskResultModel.result[AdcTaskResultField.RightColumns].op("<@")(
                cast(filters.right_columns, JSONB)
            )
            if filters.right_columns
            else None,
        ]
