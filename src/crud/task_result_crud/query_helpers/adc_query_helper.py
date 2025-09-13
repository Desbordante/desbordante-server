from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import JSONB

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
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
            case AdcTaskResultOrderingField.LhsItemNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                    f"$[*].lhs_item.{ColumnField.Name}",
                )
            case AdcTaskResultOrderingField.RhsItemNames:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                    f"$[*].rhs_item.{ColumnField.Name}",
                )
            case AdcTaskResultOrderingField.LhsItemIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                    f"$[*].lhs_item.{ColumnField.Index}",
                )
            case AdcTaskResultOrderingField.RhsItemIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                    f"$[*].rhs_item.{ColumnField.Index}",
                )
            case AdcTaskResultOrderingField.NumberOfConjuncts:
                return func.jsonb_array_length(
                    TaskResultModel.result[AdcTaskResultItemField.Conjuncts]
                )

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AdcTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result[AdcTaskResultItemField.Conjuncts].astext.icontains(
                filters.search
            )
            if filters.search
            else None,
            # lhs_item_names
            func.jsonb_path_query_array(
                TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                f"$[*].lhs_item.{ColumnField.Name}",
            ).op("<@")(cast(filters.lhs_item_names, JSONB))
            if filters.lhs_item_names
            else None,
            # rhs_item_names
            func.jsonb_path_query_array(
                TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                f"$[*].rhs_item.{ColumnField.Name}",
            ).op("<@")(cast(filters.rhs_item_names, JSONB))
            if filters.rhs_item_names
            else None,
            # lhs_item_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                f"$[*].lhs_item.{ColumnField.Index}",
            ).op("<@")(cast(filters.lhs_item_indices, JSONB))
            if filters.lhs_item_indices
            else None,
            # rhs_item_indices
            func.jsonb_path_query_array(
                TaskResultModel.result[AdcTaskResultItemField.Conjuncts],
                f"$[*].rhs_item.{ColumnField.Index}",
            ).op("<@")(cast(filters.rhs_item_indices, JSONB))
            if filters.rhs_item_indices
            else None,
        ]
