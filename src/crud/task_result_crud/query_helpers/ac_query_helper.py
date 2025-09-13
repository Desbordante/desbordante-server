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
            case AcTaskResultOrderingField.LhsIndex:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.LhsIndex], sa.Integer
                )
            case AcTaskResultOrderingField.RhsIndex:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.RhsIndex],
                    sa.Integer,
                )
            case AcTaskResultOrderingField.LhsColumn:
                return TaskResultModel.result[AcTaskResultItemField.LhsColumn].astext
            case AcTaskResultOrderingField.RhsColumn:
                return TaskResultModel.result[AcTaskResultItemField.RhsColumn].astext
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
            # lhs_index
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.LhsIndex], sa.Integer
            ).in_(filters.lhs_indices)
            if filters.lhs_indices
            else None,
            # rhs_index
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.RhsIndex], sa.Integer
            ).in_(filters.rhs_indices)
            if filters.rhs_indices
            else None,
            # lhs_column
            TaskResultModel.result[AcTaskResultItemField.LhsColumn].astext.in_(
                filters.lhs_columns
            )
            if filters.lhs_columns
            else None,
            # rhs_column
            TaskResultModel.result[AcTaskResultItemField.RhsColumn].astext.in_(
                filters.rhs_columns
            )
            if filters.rhs_columns
            else None,
        ]
