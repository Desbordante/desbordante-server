import sqlalchemy
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import JSONB

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.fd.task_result import (
    FdTaskResultFiltersSchema,
    FdTaskResultItemField,
    FdTaskResultOrderingField,
)


class FdQueryHelper(
    BaseQueryHelper[FdTaskResultOrderingField, FdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: FdTaskResultOrderingField):
        match order_by:
            case FdTaskResultOrderingField.LhsIndices:
                return TaskResultModel.result[FdTaskResultItemField.LhsIndices].astext
            case FdTaskResultOrderingField.LhsColumns:
                return TaskResultModel.result[FdTaskResultItemField.LhsColumns].astext
            case FdTaskResultOrderingField.RhsIndex:
                return func.cast(
                    TaskResultModel.result[FdTaskResultItemField.RhsIndex].astext,
                    sqlalchemy.Integer,
                )
            case FdTaskResultOrderingField.RhsColumn:
                return TaskResultModel.result[FdTaskResultItemField.RhsColumn].astext
            case FdTaskResultOrderingField.NumberOfLhsColumns:
                return func.jsonb_array_length(
                    TaskResultModel.result[FdTaskResultItemField.LhsColumns]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: FdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[
                    FdTaskResultItemField.LhsColumns
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    FdTaskResultItemField.RhsColumn
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # lhs_columns
            TaskResultModel.result[FdTaskResultItemField.LhsColumns].op("<@")(
                cast(filters.lhs_columns, JSONB)
            )
            if filters.lhs_columns
            else None,
            # lhs_indices
            TaskResultModel.result[FdTaskResultItemField.LhsIndices].op("<@")(
                cast(filters.lhs_indices, JSONB)
            )
            if filters.lhs_indices
            else None,
            # rhs_index
            func.cast(
                TaskResultModel.result[FdTaskResultItemField.RhsIndex].astext,
                sqlalchemy.Integer,
            )
            == filters.rhs_index
            if filters.rhs_index is not None
            else None,
            # rhs_column
            TaskResultModel.result[FdTaskResultItemField.RhsColumn].astext
            == filters.rhs_column
            if filters.rhs_column
            else None,
        ]
