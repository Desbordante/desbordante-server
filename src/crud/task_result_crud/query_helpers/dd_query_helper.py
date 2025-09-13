import sqlalchemy as sa
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.dd.task_result import (
    DdTaskResultFiltersSchema,
    DdTaskResultItemField,
    DdTaskResultOrderingField,
)


class DdQueryHelper(
    BaseQueryHelper[DdTaskResultOrderingField, DdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: DdTaskResultOrderingField):
        match order_by:
            case DdTaskResultOrderingField.NumberOfLhsItems:
                return func.jsonb_array_length(
                    TaskResultModel.result[DdTaskResultItemField.LhsItems]
                )
            case DdTaskResultOrderingField.LhsColumnNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result,
                    f"$.{DdTaskResultItemField.LhsItems}[*].column_name",
                )
            case DdTaskResultOrderingField.LhsColumnIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result,
                    f"$.{DdTaskResultItemField.LhsItems}[*].column_index",
                )
            case DdTaskResultOrderingField.RhsColumnNames:
                return TaskResultModel.result[DdTaskResultItemField.RhsItem][
                    "column_name"
                ].astext
            case DdTaskResultOrderingField.RhsColumnIndices:
                return func.cast(
                    TaskResultModel.result[DdTaskResultItemField.RhsItem][
                        "column_index"
                    ],
                    sa.Integer,
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: DdTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # lhs_column_names
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.LhsItems}[*].column_name",
            ).op("<@")(filters.lhs_column_names)
            if filters.lhs_column_names
            else None,
            # lhs_column_indices
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.LhsItems}[*].column_index",
            ).op("<@")(filters.lhs_column_indices)
            if filters.lhs_column_indices
            else None,
            # rhs_column_names
            TaskResultModel.result[DdTaskResultItemField.RhsItem][
                "column_name"
            ].astext.in_(filters.rhs_column_names)
            if filters.rhs_column_names
            else None,
            # rhs_column_indices
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.RhsItem}[*].column_index",
            ).op("<@")(filters.rhs_column_indices)
            if filters.rhs_column_indices
            else None,
        ]
