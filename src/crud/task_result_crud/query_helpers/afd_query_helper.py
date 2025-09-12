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
            case AfdTaskResultOrderingField.LeftIndices:
                return TaskResultModel.result[AfdTaskResultItemField.LeftIndices].astext
            case AfdTaskResultOrderingField.LeftColumns:
                return TaskResultModel.result[AfdTaskResultItemField.LeftColumns].astext
            case AfdTaskResultOrderingField.RightIndex:
                return func.cast(
                    TaskResultModel.result[AfdTaskResultItemField.RightIndex].astext,
                    sqlalchemy.Integer,
                )
            case AfdTaskResultOrderingField.RightColumn:
                return TaskResultModel.result[AfdTaskResultItemField.RightColumn].astext
            case AfdTaskResultOrderingField.NumberOfLeftColumns:
                return func.jsonb_array_length(
                    TaskResultModel.result[AfdTaskResultItemField.LeftColumns]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AfdTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[
                    AfdTaskResultItemField.LeftColumns
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    AfdTaskResultItemField.RightColumn
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # left_columns
            TaskResultModel.result[AfdTaskResultItemField.LeftColumns].op("<@")(
                cast(filters.left_columns, JSONB)
            )
            if filters.left_columns
            else None,
            # left_indices
            TaskResultModel.result[AfdTaskResultItemField.LeftIndices].op("<@")(
                cast(filters.left_indices, JSONB)
            )
            if filters.left_indices
            else None,
            # right_index
            func.cast(
                TaskResultModel.result[AfdTaskResultItemField.RightIndex].astext,
                sqlalchemy.Integer,
            )
            == filters.right_index
            if filters.right_index is not None
            else None,
            # right_column
            TaskResultModel.result[AfdTaskResultItemField.RightColumn].astext
            == filters.right_column
            if filters.right_column
            else None,
        ]
