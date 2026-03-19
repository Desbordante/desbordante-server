from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import JSONB, JSONPATH

from src.crud.profiling_dep_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_models import ProfilingDepModel
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcTaskResultFiltersSchema,
    AdcTaskResultItemField,
    AdcTaskResultOrderingField,
)
from src.schemas.task_schemas.primitives.base_schemas import ColumnField


class AdcQueryHelper(
    BaseQueryHelper[AdcTaskResultOrderingField, AdcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AdcTaskResultOrderingField):
        match order_by:
            case AdcTaskResultOrderingField.LHS_ITEM_NAMES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                    cast(f"$[*].lhs_item.{ColumnField.NAME}", JSONPATH),
                )
            case AdcTaskResultOrderingField.RHS_ITEM_NAMES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                    cast(f"$[*].rhs_item.{ColumnField.NAME}", JSONPATH),
                )
            case AdcTaskResultOrderingField.LHS_ITEM_INDICES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                    cast(f"$[*].lhs_item.{ColumnField.INDEX}", JSONPATH),
                )
            case AdcTaskResultOrderingField.RHS_ITEM_INDICES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                    cast(f"$[*].rhs_item.{ColumnField.INDEX}", JSONPATH),
                )
            case AdcTaskResultOrderingField.NUMBER_OF_CONJUNCTS:
                return func.jsonb_array_length(
                    ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AdcTaskResultFiltersSchema):
        return [
            # search
            ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS].astext.icontains(
                filters.search
            )
            if filters.search
            else None,
            # lhs_item_names
            func.jsonb_path_query_array(
                ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                cast(f"$[*].lhs_item.{ColumnField.NAME}", JSONPATH),
            ).op("<@")(cast(filters.lhs_item_names, JSONB))
            if filters.lhs_item_names
            else None,
            # rhs_item_names
            func.jsonb_path_query_array(
                ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                cast(f"$[*].rhs_item.{ColumnField.NAME}", JSONPATH),
            ).op("<@")(cast(filters.rhs_item_names, JSONB))
            if filters.rhs_item_names
            else None,
            # lhs_item_indices
            func.jsonb_path_query_array(
                ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                cast(f"$[*].lhs_item.{ColumnField.INDEX}", JSONPATH),
            ).op("<@")(cast(filters.lhs_item_indices, JSONB))
            if filters.lhs_item_indices
            else None,
            # rhs_item_indices
            func.jsonb_path_query_array(
                ProfilingDepModel.result[AdcTaskResultItemField.CONJUNCTS],
                cast(f"$[*].rhs_item.{ColumnField.INDEX}", JSONPATH),
            ).op("<@")(cast(filters.rhs_item_indices, JSONB))
            if filters.rhs_item_indices
            else None,
        ]
