import sqlalchemy as sa
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import JSONB, JSONPATH

from src.crud.profiling_dep_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_models import ProfilingDepModel
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
                    ProfilingDepModel.result[DdTaskResultItemField.LHS_ITEMS]
                )
            case DdTaskResultOrderingField.LHS_ITEMS_NAMES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result,
                    cast(
                        f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.NAME}",
                        JSONPATH,
                    ),
                )
            case DdTaskResultOrderingField.LHS_ITEMS_INDICES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result,
                    cast(
                        f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.INDEX}",
                        JSONPATH,
                    ),
                )
            case DdTaskResultOrderingField.RHS_ITEM_NAMES:
                return ProfilingDepModel.result[DdTaskResultItemField.RHS_ITEM][
                    ColumnField.NAME
                ].astext
            case DdTaskResultOrderingField.RHS_ITEM_INDICES:
                return func.cast(
                    ProfilingDepModel.result[DdTaskResultItemField.RHS_ITEM][
                        ColumnField.INDEX
                    ],
                    sa.Integer,
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: DdTaskResultFiltersSchema):
        return [
            # search
            or_(
                ProfilingDepModel.result[
                    DdTaskResultItemField.LHS_ITEMS
                ].astext.icontains(filters.search),
                ProfilingDepModel.result[
                    DdTaskResultItemField.RHS_ITEM
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # lhs_column_names
            func.jsonb_path_query_array(
                ProfilingDepModel.result,
                cast(
                    f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.NAME}",
                    JSONPATH,
                ),
            ).op("<@")(cast(filters.lhs_items_names, JSONB))
            if filters.lhs_items_names
            else None,
            # lhs_column_indices
            func.jsonb_path_query_array(
                ProfilingDepModel.result,
                cast(
                    f"$.{DdTaskResultItemField.LHS_ITEMS}[*].{ColumnField.INDEX}",
                    JSONPATH,
                ),
            ).op("<@")(cast(filters.lhs_items_indices, JSONB))
            if filters.lhs_items_indices
            else None,
            # rhs_column_names
            ProfilingDepModel.result[DdTaskResultItemField.RHS_ITEM][
                ColumnField.NAME
            ].astext.in_(filters.rhs_item_names)
            if filters.rhs_item_names
            else None,
            # rhs_column_indices
            func.jsonb_path_query_array(
                ProfilingDepModel.result,
                cast(
                    f"$.{DdTaskResultItemField.RHS_ITEM}.{ColumnField.INDEX}",
                    JSONPATH,
                ),
            ).op("<@")(cast(filters.rhs_item_indices, JSONB))
            if filters.rhs_item_indices
            else None,
        ]
