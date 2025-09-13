import sqlalchemy as sa
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.ac.task_result import (
    AcTaskResultFiltersSchema,
    AcTaskResultItemField,
    AcTaskResultOrderingField,
)
from src.schemas.task_schemas.primitives.base_schemas import ColumnField


class AcQueryHelper(
    BaseQueryHelper[AcTaskResultOrderingField, AcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AcTaskResultOrderingField):
        match order_by:
            case AcTaskResultOrderingField.LhsColumnIndex:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.LhsColumn][
                        ColumnField.Index
                    ],
                    sa.Integer,
                )
            case AcTaskResultOrderingField.RhsColumnIndex:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.RhsColumn][
                        ColumnField.Index
                    ],
                    sa.Integer,
                )
            case AcTaskResultOrderingField.LhsColumnName:
                return TaskResultModel.result[AcTaskResultItemField.LhsColumn][
                    ColumnField.Name
                ].astext
            case AcTaskResultOrderingField.RhsColumnName:
                return TaskResultModel.result[AcTaskResultItemField.RhsColumn][
                    ColumnField.Name
                ].astext

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
            # lhs_column_indices
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.LhsColumn][
                    ColumnField.Index
                ],
                sa.Integer,
            ).in_(filters.lhs_column_indices)
            if filters.lhs_column_indices
            else None,
            # rhs_column_indices
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.RhsColumn][
                    ColumnField.Index
                ],
                sa.Integer,
            ).in_(filters.rhs_column_indices)
            if filters.rhs_column_indices
            else None,
            # lhs_column_names
            TaskResultModel.result[AcTaskResultItemField.LhsColumn][
                ColumnField.Name
            ].astext.in_(filters.lhs_column_names)
            if filters.lhs_column_names
            else None,
            # rhs_column_names
            TaskResultModel.result[AcTaskResultItemField.RhsColumn][
                ColumnField.Name
            ].astext.in_(filters.rhs_column_names)
            if filters.rhs_column_names
            else None,
        ]
