from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.adc.task_result import (
    AdcTaskResultFiltersSchema,
    AdcTaskResultOrderingField,
)


class AdcQueryHelper(
    BaseQueryHelper[AdcTaskResultOrderingField, AdcTaskResultFiltersSchema]
):
    def get_ordering_field(self, order_by: AdcTaskResultOrderingField):
        match order_by:
            case AdcTaskResultOrderingField.Length:
                return func.jsonb_array_length(TaskResultModel.result["cojuncts"])

        super().get_ordering_field(order_by)

    def make_filters(self, filters: AdcTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result["cojuncts"].astext.icontains(filters.search)
            if filters.search
            else None,
        ]
