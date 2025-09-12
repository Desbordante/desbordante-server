import sqlalchemy as sa
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.ac.task_result import (
    AcTaskResultFiltersSchema,
    AcTaskResultItemField,
    AcTaskResultOrderingField,
)


class AcQueryHelper(
    BaseQueryHelper[AcTaskResultOrderingField, AcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AcTaskResultOrderingField):
        match order_by:
            case AcTaskResultOrderingField.LeftIndex:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.LeftIndex], sa.Integer
                )
            case AcTaskResultOrderingField.RightIndex:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.RightIndex],
                    sa.Integer,
                )
            case AcTaskResultOrderingField.LeftColumn:
                return TaskResultModel.result[AcTaskResultItemField.LeftColumn].astext
            case AcTaskResultOrderingField.RightColumn:
                return TaskResultModel.result[AcTaskResultItemField.RightColumn].astext
            case AcTaskResultOrderingField.NumberOfRanges:
                return func.jsonb_array_length(
                    TaskResultModel.result[AcTaskResultItemField.Ranges]
                )
            case AcTaskResultOrderingField.NumberOfExceptions:
                return func.jsonb_array_length(
                    TaskResultModel.result[AcTaskResultItemField.Exceptions]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AcTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # left_index
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.LeftIndex], sa.Integer
            ).in_(filters.left_indices)
            if filters.left_indices
            else None,
            # right_index
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.RightIndex], sa.Integer
            ).in_(filters.right_indices)
            if filters.right_indices
            else None,
            # left_column
            TaskResultModel.result[AcTaskResultItemField.LeftColumn].astext.in_(
                filters.left_columns
            )
            if filters.left_columns
            else None,
            # right_column
            TaskResultModel.result[AcTaskResultItemField.RightColumn].astext.in_(
                filters.right_columns
            )
            if filters.right_columns
            else None,
        ]
