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
            case AcTaskResultOrderingField.LHS_COLUMN_INDEX:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.LHS_COLUMN][
                        ColumnField.INDEX
                    ],
                    sa.Integer,
                )
            case AcTaskResultOrderingField.RHS_COLUMN_INDEX:
                return func.cast(
                    TaskResultModel.result[AcTaskResultItemField.RHS_COLUMN][
                        ColumnField.INDEX
                    ],
                    sa.Integer,
                )
            case AcTaskResultOrderingField.LHS_COLUMN_NAME:
                return TaskResultModel.result[AcTaskResultItemField.LHS_COLUMN][
                    ColumnField.NAME
                ].astext
            case AcTaskResultOrderingField.RHS_COLUMN_NAME:
                return TaskResultModel.result[AcTaskResultItemField.RHS_COLUMN][
                    ColumnField.NAME
                ].astext

            case AcTaskResultOrderingField.NUMBER_OF_RANGES:
                return func.jsonb_array_length(
                    TaskResultModel.result[AcTaskResultItemField.RANGES]
                )
            case AcTaskResultOrderingField.NUMBER_OF_EXCEPTIONS:
                return func.jsonb_array_length(
                    TaskResultModel.result[AcTaskResultItemField.EXCEPTIONS]
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
                TaskResultModel.result[AcTaskResultItemField.LHS_COLUMN][
                    ColumnField.INDEX
                ],
                sa.Integer,
            ).in_(filters.lhs_column_indices)
            if filters.lhs_column_indices
            else None,
            # rhs_column_indices
            func.cast(
                TaskResultModel.result[AcTaskResultItemField.RHS_COLUMN][
                    ColumnField.INDEX
                ],
                sa.Integer,
            ).in_(filters.rhs_column_indices)
            if filters.rhs_column_indices
            else None,
            # lhs_column_names
            TaskResultModel.result[AcTaskResultItemField.LHS_COLUMN][
                ColumnField.NAME
            ].astext.in_(filters.lhs_column_names)
            if filters.lhs_column_names
            else None,
            # rhs_column_names
            TaskResultModel.result[AcTaskResultItemField.RHS_COLUMN][
                ColumnField.NAME
            ].astext.in_(filters.rhs_column_names)
            if filters.rhs_column_names
            else None,
        ]
