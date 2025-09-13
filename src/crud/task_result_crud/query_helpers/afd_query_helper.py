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
from src.schemas.task_schemas.primitives.base_schemas import ColumnField


class AfdQueryHelper(
    BaseQueryHelper[AfdTaskResultOrderingField, AfdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AfdTaskResultOrderingField):
        match order_by:
            case AfdTaskResultOrderingField.LhsColumnsIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[AfdTaskResultItemField.LhsColumns],
                    f"$[*].{ColumnField.Index}",
                )
            case AfdTaskResultOrderingField.LhsColumnsNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[AfdTaskResultItemField.LhsColumns],
                    f"$[*].{ColumnField.Name}",
                )
            case AfdTaskResultOrderingField.RhsColumnIndex:
                return func.cast(
                    TaskResultModel.result[AfdTaskResultItemField.RhsColumn][
                        ColumnField.Index
                    ].astext,
                    sqlalchemy.Integer,
                )
            case AfdTaskResultOrderingField.RhsColumnName:
                return TaskResultModel.result[AfdTaskResultItemField.RhsColumn][
                    ColumnField.Name
                ].astext
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
            # lhs_columns_names
            func.jsonb_path_query_array(
                TaskResultModel.result[AfdTaskResultItemField.LhsColumns],
                f"$[*].{ColumnField.Name}",
            ).op("<@")(cast(filters.lhs_columns_names, JSONB))
            if filters.lhs_columns_names
            else None,
            # lhs_columns_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[AfdTaskResultItemField.LhsColumns],
                f"$[*].{ColumnField.Index}",
            ).op("<@")(cast(filters.lhs_columns_indices, JSONB))
            if filters.lhs_columns_indices
            else None,
            # rhs_column_index
            func.cast(
                TaskResultModel.result[AfdTaskResultItemField.RhsColumn][
                    ColumnField.Index
                ].astext,
                sqlalchemy.Integer,
            )
            == filters.rhs_column_index
            if filters.rhs_column_index is not None
            else None,
            # rhs_column_name
            TaskResultModel.result[AfdTaskResultItemField.RhsColumn][
                ColumnField.Name
            ].astext
            == filters.rhs_column_name
            if filters.rhs_column_name
            else None,
        ]
