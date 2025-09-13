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
            case MfdVerificationTaskResultOrderingField.LhsValues:
                return TaskResultModel.result[
                    MfdVerificationTaskResultItemField.LhsValues
                ].astext
            case MfdVerificationTaskResultOrderingField.MaxDistance:
                return func.cast(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.MaxDistance
                    ],
                    sa.Float,
                )
            case MfdVerificationTaskResultOrderingField.ClusterIndex:
                return func.cast(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.ClusterIndex
                    ],
                    sa.Integer,
                )
            case MfdVerificationTaskResultOrderingField.HighlightsDataIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.Highlights
                    ],
                    f"$[*].{MfdVerificationHighlightField.DataIndex}",
                )
            case MfdVerificationTaskResultOrderingField.HighlightsFurthestDataIndices:
                return func.jsonb_path_query_array(
                    TaskResultModel.result[
                        MfdVerificationTaskResultItemField.Highlights
                    ],
                    f"$[*].{MfdVerificationHighlightField.FurthestDataIndex}",
                )

        return super().get_ordering_field(order_by)

    def make_filters(self, filters: MfdVerificationTaskResultFiltersSchema):
        return [
            # search
            TaskResultModel.result.astext.icontains(filters.search)
            if filters.search
            else None,
            # cluster_indices
            TaskResultModel.result[MfdVerificationTaskResultItemField.ClusterIndex].in_(
                filters.cluster_indices
            )
            if filters.cluster_indices
            else None,
        ]
