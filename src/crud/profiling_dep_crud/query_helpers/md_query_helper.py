from sqlalchemy import (
    cast,
    column,
    func,
    or_,
)
from sqlalchemy.dialects.postgresql import JSONPATH

from src.crud.profiling_dep_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_models import ProfilingDepModel
from src.schemas.task_schemas.primitives.md.task_result import (
    MdTaskResultFiltersSchema,
    MdTaskResultItemField,
    MdTaskResultOrderingField,
    MdTaskResultSideItemField,
)


class MdQueryHelper(
    BaseQueryHelper[MdTaskResultOrderingField, MdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: MdTaskResultOrderingField):
        match order_by:
            case MdTaskResultOrderingField.NUMBER_OF_LHS_ITEMS:
                return func.jsonb_array_length(
                    ProfilingDepModel.result[MdTaskResultItemField.LHS_ITEMS]
                )
            case MdTaskResultOrderingField.LHS_ITEMS_METRICS:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[MdTaskResultItemField.LHS_ITEMS],
                    cast(
                        f"$[*].{MdTaskResultSideItemField.METRIC}",
                        JSONPATH,
                    ),
                )
            case MdTaskResultOrderingField.LHS_ITEMS_BOUNDARIES:
                return func.jsonb_path_query_array(
                    ProfilingDepModel.result[MdTaskResultItemField.LHS_ITEMS],
                    cast(
                        f"$[*].{MdTaskResultSideItemField.BOUNDARY}",
                        JSONPATH,
                    ),
                )
            case MdTaskResultOrderingField.RHS_ITEM_METRIC:
                return ProfilingDepModel.result[MdTaskResultItemField.RHS_ITEM][
                    MdTaskResultSideItemField.METRIC
                ]
            case MdTaskResultOrderingField.RHS_ITEM_BOUNDARY:
                return ProfilingDepModel.result[MdTaskResultItemField.RHS_ITEM][
                    MdTaskResultSideItemField.BOUNDARY
                ]

        super().get_ordering_field(order_by)

    def make_filters(self, filters: MdTaskResultFiltersSchema):
        return [
            # search
            or_(
                ProfilingDepModel.result[
                    MdTaskResultItemField.LHS_ITEMS
                ].astext.icontains(filters.search),
                ProfilingDepModel.result[
                    MdTaskResultItemField.RHS_ITEM
                ].astext.icontains(filters.search),
            )
            if filters.search
            else None,
            # lhs_items_metrics
            func.jsonb_array_length(
                column("result").op("->")(MdTaskResultItemField.LHS_ITEMS)
            )
            > 0
            if filters.lhs_items_metrics
            else None,
            # rhs_item_metrics
            ProfilingDepModel.result[MdTaskResultItemField.RHS_ITEM][
                MdTaskResultSideItemField.METRIC
            ].in_(filters.rhs_item_metrics)
            if filters.rhs_item_metrics
            else None,
        ]

    def get_filtered_result_column(self, filters: MdTaskResultFiltersSchema):
        conditions = [
            "@.boundary != 0" if filters.show_zeroes is False else None,
            (
                f"({' || '.join([f'@.metric == "{metric}"' for metric in filters.lhs_items_metrics])})"
            )
            if filters.lhs_items_metrics
            else None,
        ]

        conditions = [c for c in conditions if c is not None]

        if not conditions:
            return super().get_filtered_result_column(filters)

        condition = cast(
            f"$[*] ? ({' && '.join(conditions)})",
            JSONPATH,
        )

        return func.jsonb_build_object(
            MdTaskResultItemField.LHS_ITEMS,
            func.jsonb_path_query_array(
                ProfilingDepModel.result[MdTaskResultItemField.LHS_ITEMS],
                condition,
            ),
            MdTaskResultItemField.RHS_ITEM,
            ProfilingDepModel.result[MdTaskResultItemField.RHS_ITEM],
        )
