import sqlalchemy
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.dd.task_result import (
    DdTaskResultFiltersSchema,
    DdTaskResultOrderingField,
)


class DdQueryHelper(
    BaseQueryHelper[DdTaskResultOrderingField, DdTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: DdTaskResultOrderingField):
        match order_by:
            case DdTaskResultOrderingField.NumberOfLhs:
                return func.jsonb_array_length(TaskResultModel.result["lhs"])
            case DdTaskResultOrderingField.NumberOfRhs:
                return func.jsonb_array_length(TaskResultModel.result["rhs"])

        super().get_ordering_field(order_by)

    def make_filters(self, filters: DdTaskResultFiltersSchema):
        return [
            # search
            sqlalchemy.or_(
                TaskResultModel.result["lhs"].astext.icontains(filters.search),
                TaskResultModel.result["rhs"].astext.icontains(filters.search),
            )
            if filters.search
            else None,
        ]
