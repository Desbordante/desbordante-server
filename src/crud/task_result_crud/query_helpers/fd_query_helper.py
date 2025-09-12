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
            case FdTaskResultOrderingField.LeftIndices:
                return TaskResultModel.result[FdTaskResultItemField.LeftIndices].astext
            case FdTaskResultOrderingField.LeftColumns:
                return TaskResultModel.result[FdTaskResultItemField.LeftColumns].astext
            case FdTaskResultOrderingField.RightIndex:
                return func.cast(
                    TaskResultModel.result[FdTaskResultItemField.RightIndex].astext,
                    sqlalchemy.Integer,
                )
            case FdTaskResultOrderingField.RightColumn:
                return TaskResultModel.result[FdTaskResultItemField.RightColumn].astext
            case FdTaskResultOrderingField.NumberOfLeftColumns:
                return func.jsonb_array_length(
                    TaskResultModel.result[FdTaskResultItemField.LeftColumns]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: FdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[
                    FdTaskResultItemField.LeftColumns
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    FdTaskResultItemField.RightColumn
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # left_columns
            TaskResultModel.result[FdTaskResultItemField.LeftColumns].op("<@")(
                cast(filters.left_columns, JSONB)
            )
            if filters.left_columns
            else None,
            # left_indices
            TaskResultModel.result[FdTaskResultItemField.LeftIndices].op("<@")(
                cast(filters.left_indices, JSONB)
            )
            if filters.left_indices
            else None,
            # right_index
            func.cast(
                TaskResultModel.result[FdTaskResultItemField.RightIndex].astext,
                sqlalchemy.Integer,
            )
            == filters.right_index
            if filters.right_index is not None
            else None,
            # right_column
            TaskResultModel.result[FdTaskResultItemField.RightColumn].astext
            == filters.right_column
            if filters.right_column
            else None,
        ]
