import sqlalchemy
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.ac.task_result import (
    AcResultType,
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
            case AcTaskResultOrderingField.Ranges:
                return TaskResultModel.result[order_by].astext
            case AcTaskResultOrderingField.ColumnPairs:
                return TaskResultModel.result[order_by].astext
            case AcTaskResultOrderingField.ColumnPairsNames:
                return TaskResultModel.result[order_by].astext
            case AcTaskResultOrderingField.RowIndex:
                return func.cast(
                    TaskResultModel.result[order_by].astext, sqlalchemy.Integer
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AcTaskResultFiltersSchema):
        return [
            TaskResultModel.result["type"].astext == filters.type.value,
            # left column index
            TaskResultModel.result[AcTaskResultOrderingField.LeftColumnIndex].astext
            == str(filters.left_column_index)
            if filters.left_column_index and filters.type == AcResultType.Range
            else None,
            # right column index
            TaskResultModel.result[AcTaskResultOrderingField.RightColumnIndex].astext
            == str(filters.right_column_index)
            if filters.right_column_index and filters.type == AcResultType.Range
            else None,
            # left column name
            TaskResultModel.result[AcTaskResultOrderingField.LeftColumnName].astext
            == filters.left_column_name
            if filters.left_column_name and filters.type == AcResultType.Range
            else None,
            # right column name
            TaskResultModel.result[AcTaskResultOrderingField.RightColumnName].astext
            == filters.right_column_name
            if filters.right_column_name and filters.type == AcResultType.Range
            else None,
        ]
