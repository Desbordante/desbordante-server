import sqlalchemy as sa
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.base_schemas import ColumnField
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
            case DdTaskResultOrderingField.LhsItemsNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result,
                    f"$.{DdTaskResultItemField.LhsItems}[*].{ColumnField.Name}",
                )
            case DdTaskResultOrderingField.LhsItemsIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result,
                    f"$.{DdTaskResultItemField.LhsItems}[*].{ColumnField.Index}",
                )
            case DdTaskResultOrderingField.RhsItemNames:
                return TaskResultModel.result[DdTaskResultItemField.RhsItem][
                    ColumnField.Name
                ].astext
            case DdTaskResultOrderingField.RhsItemIndices:
                return func.cast(
                    TaskResultModel.result[DdTaskResultItemField.RhsItem][
                        ColumnField.Index
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
                f"$.{DdTaskResultItemField.LhsItems}[*].{ColumnField.Name}",
            ).op("<@")(filters.lhs_items_names)
            if filters.lhs_items_names
            else None,
            # lhs_column_indices
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.LhsItems}[*].{ColumnField.Index}",
            ).op("<@")(filters.lhs_items_indices)
            if filters.lhs_items_indices
            else None,
            # rhs_column_names
            TaskResultModel.result[DdTaskResultItemField.RhsItem][
                ColumnField.Name
            ].astext.in_(filters.rhs_item_names)
            if filters.rhs_item_names
            else None,
            # rhs_column_indices
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.RhsItem}[*].{ColumnField.Index}",
            ).op("<@")(filters.rhs_item_indices)
            if filters.rhs_item_indices
            else None,
        ]
