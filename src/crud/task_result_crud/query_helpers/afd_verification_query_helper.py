from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.schemas.task_schemas.afd_verification.task_result import (
    AfdVerificationTaskResultFiltersSchema,
    AfdVerificationTaskResultOrderingField,
)


class AfdVerificationQueryHelper(
    BaseQueryHelper[
        AfdVerificationTaskResultOrderingField, AfdVerificationTaskResultFiltersSchema
    ]
):
    def get_ordering_field(self, order_by: AfdVerificationTaskResultOrderingField):
        super().get_ordering_field(order_by)

    def make_filters(self, filters: AfdVerificationTaskResultFiltersSchema):
        return []
