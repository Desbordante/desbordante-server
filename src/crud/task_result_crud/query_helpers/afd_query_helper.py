import sqlalchemy
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import JSONB

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.afd.task_result import (
    AfdTaskResultFiltersSchema,
    AfdTaskResultItemField,
    AfdTaskResultOrderingField,
)


class AfdQueryHelper(
    BaseQueryHelper[AfdTaskResultOrderingField, AfdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AfdTaskResultOrderingField):
        match order_by:
            case AfdTaskResultOrderingField.LhsIndices:
                return TaskResultModel.result[AfdTaskResultItemField.LhsIndices].astext
            case AfdTaskResultOrderingField.LhsColumns:
                return TaskResultModel.result[AfdTaskResultItemField.LhsColumns].astext
            case AfdTaskResultOrderingField.RhsIndex:
                return func.cast(
                    TaskResultModel.result[AfdTaskResultItemField.RhsIndex].astext,
                    sqlalchemy.Integer,
                )
            case AfdTaskResultOrderingField.RhsColumn:
                return TaskResultModel.result[AfdTaskResultItemField.RhsColumn].astext
            case AfdTaskResultOrderingField.NumberOfLhsColumns:
                return func.jsonb_array_length(
                    TaskResultModel.result[AfdTaskResultItemField.LhsColumns]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AfdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[
                    AfdTaskResultItemField.LhsColumns
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    AfdTaskResultItemField.RhsColumn
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # lhs_columns
            TaskResultModel.result[AfdTaskResultItemField.LhsColumns].op("<@")(
                cast(filters.lhs_columns, JSONB)
            )
            if filters.lhs_columns
            else None,
            # lhs_indices
            TaskResultModel.result[AfdTaskResultItemField.LhsIndices].op("<@")(
                cast(filters.lhs_indices, JSONB)
            )
            if filters.lhs_indices
            else None,
            # rhs_index
            func.cast(
                TaskResultModel.result[AfdTaskResultItemField.RhsIndex].astext,
                sqlalchemy.Integer,
            )
            == filters.rhs_index
            if filters.rhs_index is not None
            else None,
            # rhs_column
            TaskResultModel.result[AfdTaskResultItemField.RhsColumn].astext
            == filters.rhs_column
            if filters.rhs_column
            else None,
        ]
