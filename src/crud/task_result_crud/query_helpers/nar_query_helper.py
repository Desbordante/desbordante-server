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
            case NarTaskResultOrderingField.NumberOfLhsItems:
                return func.jsonb_array_length(NarTaskResultItemField.LhsItems)
            case NarTaskResultOrderingField.NumberOfRhsItems:
                return func.jsonb_array_length(NarTaskResultItemField.RhsItems)
            case NarTaskResultOrderingField.LhsItemsNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.LhsItems],
                    f"$[*].{ColumnField.Name}",
                )
            case NarTaskResultOrderingField.LhsItemsIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.LhsItems],
                    f"$[*].{ColumnField.Index}",
                )
            case NarTaskResultOrderingField.RhsItemsNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.RhsItems],
                    f"$[*].{ColumnField.Name}",
                )
            case NarTaskResultOrderingField.RhsItemsIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[NarTaskResultItemField.RhsItems],
                    f"$[*].{ColumnField.Index}",
                )
            case NarTaskResultOrderingField.Confidence:
                return func.cast(
                    TaskResultModel.result[NarTaskResultItemField.Confidence],
                    sqlalchemy.Float,
                )
            case NarTaskResultOrderingField.Support:
                return func.cast(
                    TaskResultModel.result[NarTaskResultItemField.Support],
                    sqlalchemy.Float,
                )
            case NarTaskResultOrderingField.Fitness:
                return func.cast(
                    TaskResultModel.result[NarTaskResultItemField.Fitness],
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
                TaskResultModel.result[NarTaskResultItemField.Confidence],
                sqlalchemy.Float,
            )
            >= filters.min_confidence
            if filters.min_confidence is not None
            else None,
            # max_confidence
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.Confidence],
                sqlalchemy.Float,
            )
            <= filters.max_confidence
            if filters.max_confidence is not None
            else None,
            # min_support
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.Support],
                sqlalchemy.Float,
            )
            >= filters.min_support
            if filters.min_support is not None
            else None,
            # max_support
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.Support],
                sqlalchemy.Float,
            )
            <= filters.max_support
            if filters.max_support is not None
            else None,
            # min_fitness
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.Fitness],
                sqlalchemy.Float,
            )
            >= filters.min_fitness
            if filters.min_fitness is not None
            else None,
            # max_fitness
            func.cast(
                TaskResultModel.result[NarTaskResultItemField.Fitness],
                sqlalchemy.Float,
            )
            <= filters.max_fitness
            if filters.max_fitness is not None
            else None,
            # lhs_items_names
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.LhsItems],
                f"$[*].{ColumnField.Name}",
            ).op("<@")(filters.lhs_items_names)
            if filters.lhs_items_names
            else None,
            # lhs_items_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.LhsItems],
                f"$[*].{ColumnField.Index}",
            ).op("<@")(filters.lhs_items_indices)
            if filters.lhs_items_indices
            else None,
            # rhs_items_names
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.RhsItems],
                f"$[*].{ColumnField.Name}",
            ).op("<@")(filters.rhs_items_names)
            if filters.rhs_items_names
            else None,
            # rhs_items_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[NarTaskResultItemField.RhsItems],
                f"$[*].{ColumnField.Index}",
            ).op("<@")(filters.rhs_items_indices)
            if filters.rhs_items_indices
            else None,
        ]
