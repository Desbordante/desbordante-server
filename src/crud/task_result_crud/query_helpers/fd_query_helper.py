import sqlalchemy
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import JSONB

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.base_schemas import ColumnField
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
            case FdTaskResultOrderingField.LhsColumnsIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[FdTaskResultItemField.LhsColumns],
                    f"$[*].{ColumnField.Index}",
                )
            case FdTaskResultOrderingField.LhsColumnsNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[FdTaskResultItemField.LhsColumns],
                    f"$[*].{ColumnField.Name}",
                )
            case FdTaskResultOrderingField.RhsColumnIndex:
                return func.cast(
                    TaskResultModel.result[FdTaskResultItemField.RhsColumn][
                        ColumnField.Index
                    ].astext,
                    sqlalchemy.Integer,
                )
            case FdTaskResultOrderingField.RhsColumnName:
                return TaskResultModel.result[FdTaskResultItemField.RhsColumn][
                    ColumnField.Name
                ].astext
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
            # lhs_columns_names
            func.jsonb_path_query_array(
                TaskResultModel.result[FdTaskResultItemField.LhsColumns],
                f"$[*].{ColumnField.Name}",
            ).op("<@")(cast(filters.lhs_columns_names, JSONB))
            if filters.lhs_columns_names
            else None,
            # lhs_columns_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[FdTaskResultItemField.LhsColumns],
                f"$[*].{ColumnField.Index}",
            ).op("<@")(cast(filters.lhs_columns_indices, JSONB))
            if filters.lhs_columns_indices
            else None,
            # rhs_column_index
            func.cast(
                TaskResultModel.result[FdTaskResultItemField.RhsColumn][
                    ColumnField.Index
                ].astext,
                sqlalchemy.Integer,
            ).in_(filters.rhs_column_indices)
            if filters.rhs_column_indices is not None
            else None,
            # rhs_column_name
            TaskResultModel.result[FdTaskResultItemField.RhsColumn][
                ColumnField.Name
            ].astext.in_(filters.rhs_column_names)
            if filters.rhs_column_names
            else None,
        ]
