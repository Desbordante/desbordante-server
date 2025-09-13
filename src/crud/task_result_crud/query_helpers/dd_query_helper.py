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
            case DdTaskResultOrderingField.NUMBER_OF_LHS_ITEMS:
                return func.jsonb_array_length(
                    TaskResultModel.result[DdTaskResultItemField.LHS_ITEMS]
                )
            case DdTaskResultOrderingField.LHS_ITEMS_NAMES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result,
                    f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.NAME}",
                )
            case DdTaskResultOrderingField.LHS_ITEMS_INDICES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result,
                    f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.INDEX}",
                )
            case DdTaskResultOrderingField.RHS_ITEM_NAMES:
                return TaskResultModel.result[DdTaskResultItemField.RHS_ITEM][
                    ColumnField.NAME
                ].astext
            case DdTaskResultOrderingField.RHS_ITEM_INDICES:
                return func.cast(
                    TaskResultModel.result[DdTaskResultItemField.RHS_ITEM][
                        ColumnField.INDEX
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
                f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.NAME}",
            ).op("<@")(filters.lhs_items_names)
            if filters.lhs_items_names
            else None,
            # lhs_column_indices
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.INDEX}",
            ).op("<@")(filters.lhs_items_indices)
            if filters.lhs_items_indices
            else None,
            # rhs_column_names
            TaskResultModel.result[DdTaskResultItemField.RHS_ITEM][
                ColumnField.NAME
            ].astext.in_(filters.rhs_item_names)
            if filters.rhs_item_names
            else None,
            # rhs_column_indices
            func.jsonb_path_query_array(
                TaskResultModel.result,
                f"$.{DdTaskResultItemField.RHS_ITEM}[*].{ColumnField.INDEX}",
            ).op("<@")(filters.rhs_item_indices)
            if filters.rhs_item_indices
            else None,
        ]
