import sqlalchemy
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
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
                return func.jsonb_array_length(NarTaskResultItemField.LHS_ITEMS)
            case NarTaskResultOrderingField.NUMBER_OF_RHS_ITEMS:
                return func.jsonb_array_length(NarTaskResultItemField.RHS_ITEMS)
            case NarTaskResultOrderingField.LHS_ITEMS_NAMES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.LHS_ITEMS],
                    f"$[*].{ColumnField.NAME}",
                )
            case NarTaskResultOrderingField.LHS_ITEMS_INDICES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.LHS_ITEMS],
                    f"$[*].{ColumnField.INDEX}",
                )
            case NarTaskResultOrderingField.RHS_ITEMS_NAMES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.RHS_ITEMS],
                    f"$[*].{ColumnField.NAME}",
                )
            case NarTaskResultOrderingField.RHS_ITEMS_INDICES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.RHS_ITEMS],
                    f"$[*].{ColumnField.INDEX}",
                )
            case NarTaskResultOrderingField.CONFIDENCE:
                return func.cast(
                    TaskResultModel.result[NarTaskResultItemField.CONFIDENCE],
                    sqlalchemy.Float,
                )
            case NarTaskResultOrderingField.SUPPORT:
                return func.cast(
                    TaskResultModel.result[NarTaskResultItemField.SUPPORT],
                    sqlalchemy.Float,
                )
            case NarTaskResultOrderingField.FITNESS:
                return func.cast(
                    TaskResultModel.result[NarTaskResultItemField.FITNESS],
                    sqlalchemy.Float,
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: NarTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # min_confidence
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.CONFIDENCE],
                sqlalchemy.Float,
            )
            >= filters.min_confidence
            if filters.min_confidence is not None
            else None,
            # max_confidence
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.CONFIDENCE],
                sqlalchemy.Float,
            )
            <= filters.max_confidence
            if filters.max_confidence is not None
            else None,
            # min_support
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.SUPPORT],
                sqlalchemy.Float,
            )
            >= filters.min_support
            if filters.min_support is not None
            else None,
            # max_support
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.SUPPORT],
                sqlalchemy.Float,
            )
            <= filters.max_support
            if filters.max_support is not None
            else None,
            # min_fitness
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.FITNESS],
                sqlalchemy.Float,
            )
            >= filters.min_fitness
            if filters.min_fitness is not None
            else None,
            # max_fitness
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.FITNESS],
                sqlalchemy.Float,
            )
            <= filters.max_fitness
            if filters.max_fitness is not None
            else None,
            # lhs_items_names
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.LHS_ITEMS],
                f"$[*].{ColumnField.NAME}",
            ).op("<@")(filters.lhs_items_names)
            if filters.lhs_items_names
            else None,
            # lhs_items_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.LHS_ITEMS],
                f"$[*].{ColumnField.INDEX}",
            ).op("<@")(filters.lhs_items_indices)
            if filters.lhs_items_indices
            else None,
            # rhs_items_names
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.RHS_ITEMS],
                f"$[*].{ColumnField.NAME}",
            ).op("<@")(filters.rhs_items_names)
            if filters.rhs_items_names
            else None,
            # rhs_items_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.RHS_ITEMS],
                f"$[*].{ColumnField.INDEX}",
            ).op("<@")(filters.rhs_items_indices)
            if filters.rhs_items_indices
            else None,
        ]
