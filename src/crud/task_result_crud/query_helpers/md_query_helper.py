from sqlalchemy import (
    cast,
    column,
    func,
)
from sqlalchemy.dialects.postgresql import JSONPATH

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
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
            case MdTaskResultOrderingField.NumberOfLhsItems:
                return func.jsonb_array_length(
                    TaskResultModel.result[MdTaskResultItemField.LhsItems]
                )
            case MdTaskResultOrderingField.LhsItemsMetrics:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[MdTaskResultItemField.LhsItems],
                    f"$[*].{MdTaskResultSideItemField.Metric}",
                )
            case MdTaskResultOrderingField.LhsItemsBoundaries:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[MdTaskResultItemField.LhsItems],
                    f"$[*].{MdTaskResultSideItemField.Boundary}",
                )
            case MdTaskResultOrderingField.RhsItemMetric:
                return TaskResultModel.result[MdTaskResultItemField.RhsItem][
                    MdTaskResultSideItemField.Metric
                ]
            case MdTaskResultOrderingField.RhsItemBoundary:
                return TaskResultModel.result[MdTaskResultItemField.RhsItem][
                    MdTaskResultSideItemField.Boundary
                ]

        super().get_ordering_field(order_by)

    def make_filters(self, filters: MdTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # lhs_items_metrics
            func.jsonb_array_length(
                column("result").op("->")(MdTaskResultItemField.LhsItems)
            )
            > 0
            if filters.lhs_items_metrics
            else None,
            # rhs_item_metrics
            TaskResultModel.result[MdTaskResultItemField.RhsItem][
                MdTaskResultSideItemField.Metric
            ].in_(filters.rhs_item_metrics)
            if filters.rhs_item_metrics
            else None,
        ]

    def get_filtered_result_column(self, filters: MdTaskResultFiltersSchema):
        conditions = [
            "@.boundary != 0" if not filters.show_zeroes else None,
            (
                f"({' || '.join([f'@.metrics == "{metric}"' for metric in filters.lhs_items_metrics])})"
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
            MdTaskResultItemField.LhsItems,
            func.jsonb_path_query_array(
                TaskResultModel.result[MdTaskResultItemField.LhsItems],
                condition,
            ),
            MdTaskResultItemField.RhsItem,
            TaskResultModel.result[MdTaskResultItemField.RhsItem],
        )
