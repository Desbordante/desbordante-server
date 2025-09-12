from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.ac.task_result import (
    AcTaskResultField,
    AcTaskResultFiltersSchema,
    AcTaskResultOrderingField,
)


class AcQueryHelper(
    BaseQueryHelper[AcTaskResultOrderingField, AcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AcTaskResultOrderingField):
        match order_by:
            case AcTaskResultOrderingField.LeftColumn:
                return TaskResultModel.result[AcTaskResultField.LeftColumn].astext
            case AcTaskResultOrderingField.RightColumn:
                return TaskResultModel.result[AcTaskResultField.RightColumn].astext
            case AcTaskResultOrderingField.NumberOfRanges:
                return func.jsonb_array_length(
                    TaskResultModel.result[AcTaskResultField.Ranges]
                )
            case AcTaskResultOrderingField.NumberOfExceptions:
                return func.jsonb_array_length(
                    TaskResultModel.result[AcTaskResultField.Exceptions]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AcTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # left column
            TaskResultModel.result[AcTaskResultField.LeftColumn].astext.in_(
                filters.left_columns
            )
            if filters.left_columns
            else None,
            # right column
            TaskResultModel.result[AcTaskResultField.RightColumn].astext.in_(
                filters.right_columns
            )
            if filters.right_columns
            else None,
        ]
