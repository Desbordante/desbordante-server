import sqlalchemy
from sqlalchemy import func, or_

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.ac.task_result import (
    AcTaskResultFiltersSchema,
    AcTaskResultOrderingField,
)


class AcQueryHelper(
    BaseQueryHelper[AcTaskResultOrderingField, AcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AcTaskResultOrderingField):
        match order_by:
            case AcTaskResultOrderingField.LeftColumnIndex:
                return func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Integer
                )
            case AcTaskResultOrderingField.LeftColumnName:
                return TaskResultModel.result[order_by].astext
            case AcTaskResultOrderingField.RightColumnIndex:
                return func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Integer
                )
            case AcTaskResultOrderingField.RightColumnName:
                return TaskResultModel.result[order_by].astext
            case AcTaskResultOrderingField.NumberOfRanges:
                return func.jsonb_array_length(TaskResultModel.result["ranges"])
            case AcTaskResultOrderingField.NumberOfExceptions:
                return func.jsonb_array_length(TaskResultModel.result["exceptions"])

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AcTaskResultFiltersSchema):
        return [
            # search
            or_(
                TaskResultModel.result[
                    AcTaskResultOrderingField.LeftColumnName
                ].astext.icontains(filters.search),
                TaskResultModel.result[
                    AcTaskResultOrderingField.RightColumnName
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # left column index
            TaskResultModel.result[AcTaskResultOrderingField.LeftColumnIndex].astext
            == str(filters.left_column_index)
            if filters.left_column_index is not None
            else None,
            # right column index
            TaskResultModel.result[AcTaskResultOrderingField.RightColumnIndex].astext
            == str(filters.right_column_index)
            if filters.right_column_index is not None
            else None,
            # left column name
            TaskResultModel.result[AcTaskResultOrderingField.LeftColumnName].astext
            == filters.left_column_name
            if filters.left_column_name
            else None,
            # right column name
            TaskResultModel.result[AcTaskResultOrderingField.RightColumnName].astext
            == filters.right_column_name
            if filters.right_column_name
            else None,
        ]
