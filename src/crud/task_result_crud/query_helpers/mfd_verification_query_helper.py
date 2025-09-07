from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.mfd_verification.task_result import (
    MfdVerificationTaskResultFiltersSchema,
    MfdVerificationTaskResultOrderingField,
)


class MfdVerificationQueryHelper(
    BaseQueryHelper[
        MfdVerificationTaskResultOrderingField, MfdVerificationTaskResultFiltersSchema
    ]
):
    def get_ordering_field(self, order_by: MfdVerificationTaskResultOrderingField):
        super().get_ordering_field(order_by)

    def make_filters(self, filters: MfdVerificationTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
        ]
