import sqlalchemy
from sqlalchemy import cast, func, or_
from sqlalchemy.dialects.postgresql import JSONB, JSONPATH

from src.crud.profiling_dep_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_models import ProfilingDepModel
from src.schemas.task_schemas.primitives.base_schemas import ColumnField
from src.schemas.task_schemas.primitives.nar.task_result import (
    NarTaskResultFiltersSchema,
    NarTaskResultItemField,
    NarTaskResultOrderingField,
)


class NarQueryHelper(
    BaseQueryHelper[NarTaskResultOrderingField, NarTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: NarTaskResultOrderingField):
        match order_by:
            case NarTaskResultOrderingField.NUMBER_OF_LHS_ITEMS:
                return func.jsonb_array_length(
                    ProfilingDepModel.result[NarTaskResultItemField.LHS_ITEMS]
                )
            case NarTaskResultOrderingField.NUMBER_OF_RHS_ITEMS:
                return func.jsonb_array_length(
                    ProfilingDepModel.result[NarTaskResultItemField.RHS_ITEMS]
                )
            case NarTaskResultOrderingField.LHS_ITEMS_NAMES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.LHS_ITEMS],
                    cast(f"$[*].{ColumnField.NAME}", JSONPATH),
                )
            case NarTaskResultOrderingField.LHS_ITEMS_INDICES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.LHS_ITEMS],
                    cast(f"$[*].{ColumnField.INDEX}", JSONPATH),
                )
            case NarTaskResultOrderingField.RHS_ITEMS_NAMES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.RHS_ITEMS],
                    cast(f"$[*].{ColumnField.NAME}", JSONPATH),
                )
            case NarTaskResultOrderingField.RHS_ITEMS_INDICES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.RHS_ITEMS],
                    cast(f"$[*].{ColumnField.INDEX}", JSONPATH),
                )
            case NarTaskResultOrderingField.CONFIDENCE:
                return func.cast(
                    ProfilingDepModel.result[NarTaskResultItemField.CONFIDENCE],
                    sqlalchemy.Float,
                )
            case NarTaskResultOrderingField.SUPPORT:
                return func.cast(
                    ProfilingDepModel.result[NarTaskResultItemField.SUPPORT],
                    sqlalchemy.Float,
                )
            case NarTaskResultOrderingField.FITNESS:
                return func.cast(
                    ProfilingDepModel.result[NarTaskResultItemField.FITNESS],
                    sqlalchemy.Float,
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: NarTaskResultFiltersSchema):
        return [
            # search
            or_(
                ProfilingDepModel.result[
                    NarTaskResultItemField.LHS_ITEMS
                ].astext.icontains(filters.search),
                ProfilingDepModel.result[
                    NarTaskResultItemField.RHS_ITEMS
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # min_confidence
            func.cast(
                ProfilingDepModel.result[NarTaskResultItemField.CONFIDENCE],
                sqlalchemy.Float,
            )
            >= filters.min_confidence
            if filters.min_confidence is not None
            else None,
            # max_confidence
            func.cast(
                ProfilingDepModel.result[NarTaskResultItemField.CONFIDENCE],
                sqlalchemy.Float,
            )
            <= filters.max_confidence
            if filters.max_confidence is not None
            else None,
            # min_support
            func.cast(
                ProfilingDepModel.result[NarTaskResultItemField.SUPPORT],
                sqlalchemy.Float,
            )
            >= filters.min_support
            if filters.min_support is not None
            else None,
            # max_support
            func.cast(
                ProfilingDepModel.result[NarTaskResultItemField.SUPPORT],
                sqlalchemy.Float,
            )
            <= filters.max_support
            if filters.max_support is not None
            else None,
            # min_fitness
            func.cast(
                ProfilingDepModel.result[NarTaskResultItemField.FITNESS],
                sqlalchemy.Float,
            )
            >= filters.min_fitness
            if filters.min_fitness is not None
            else None,
            # max_fitness
            func.cast(
                ProfilingDepModel.result[NarTaskResultItemField.FITNESS],
                sqlalchemy.Float,
            )
            <= filters.max_fitness
            if filters.max_fitness is not None
            else None,
            # lhs_items_names (filter array contained in result array)
            cast(filters.lhs_items_names, JSONB).op("<@")(
                func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.LHS_ITEMS],
                    cast(f"$[*].{ColumnField.NAME}", JSONPATH),
                )
            )
            if filters.lhs_items_names
            else None,
            # lhs_items_indices
            cast(filters.lhs_items_indices, JSONB).op("<@")(
                func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.LHS_ITEMS],
                    cast(f"$[*].{ColumnField.INDEX}", JSONPATH),
                )
            )
            if filters.lhs_items_indices
            else None,
            # rhs_items_names
            cast(filters.rhs_items_names, JSONB).op("<@")(
                func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.RHS_ITEMS],
                    cast(f"$[*].{ColumnField.NAME}", JSONPATH),
                )
            )
            if filters.rhs_items_names
            else None,
            # rhs_items_indices
            cast(filters.rhs_items_indices, JSONB).op("<@")(
                func.jsonb_path_query_array(
                    ProfilingDepModel.result[NarTaskResultItemField.RHS_ITEMS],
                    cast(f"$[*].{ColumnField.INDEX}", JSONPATH),
                )
            )
            if filters.rhs_items_indices
            else None,
        ]
