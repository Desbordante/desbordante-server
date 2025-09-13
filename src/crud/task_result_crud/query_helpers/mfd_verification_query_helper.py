import sqlalchemy as sa
from sqlalchemy import func

from src.crud.task_result_crud.query_helpers.base_query_helper import BaseQueryHelper
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.primitives.mfd_verification.task_result import (
    MfdVerificationHighlightField,
    MfdVerificationTaskResultFiltersSchema,
    MfdVerificationTaskResultItemField,
    MfdVerificationTaskResultOrderingField,
)


class MfdVerificationQueryHelper(
    BaseQueryHelper[
        MfdVerificationTaskResultOrderingField, MfdVerificationTaskResultFiltersSchema
    ]
):
    def get_ordering_field(self, order_by: MfdVerificationTaskResultOrderingField):
        match order_by:
            case MfdVerificationTaskResultOrderingField.LHS_VALUES:
                return TaskResultModel.result[
                    MfdVerificationTaskResultItemField.LHS_VALUES
                ].astext
            case MfdVerificationTaskResultOrderingField.MAX_DISTANCE:
                return func.cast(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.MAX_DISTANCE
                    ],
                    sa.Float,
                )
            case MfdVerificationTaskResultOrderingField.CLUSTER_INDEX:
                return func.cast(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.CLUSTER_INDEX
                    ],
                    sa.Integer,
                )
            case MfdVerificationTaskResultOrderingField.HIGHLIGHTS_DATA_INDICES:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.HIGHLIGHTS
                    ],
                    f"$[*].{MfdVerificationHighlightField.DATA_INDEX}",
                )
            case (
                MfdVerificationTaskResultOrderingField.HIGHLIGHTS_FURTHEST_DATA_INDICES
            ):
                return func.jsonb_path_query_array(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.HIGHLIGHTS
                    ],
                    f"$[*].{MfdVerificationHighlightField.FURTHEST_DATA_INDEX}",
                )

        return super().get_ordering_field(order_by)

    def make_filters(self, filters: MfdVerificationTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # cluster_indices
            TaskResultModel.result[
                MfdVerificationTaskResultItemField.CLUSTER_INDEX
            ].in_(filters.cluster_indices)
            if filters.cluster_indices
            else None,
        ]
