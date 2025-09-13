import pandas as pd
from desbordante.mfd_verification import Highlight
from desbordante.mfd_verification.algorithms import MetricVerifier

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.mfd_verification.algo_name import (
    MfdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.mfd_verification.task_params import (
    MfdVerificationTaskParams,
)
from src.schemas.task_schemas.primitives.mfd_verification.task_result import (
    MfdVerificationHighlightSchema,
    MfdVerificationTaskResultItemSchema,
    MfdVerificationTaskResultSchema,
)


class MfdVerificationPrimitive(
    BasePrimitive[
        MetricVerifier,
        MfdVerificationAlgoName,
        MfdVerificationTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[
            MfdVerificationTaskResultSchema, MfdVerificationTaskResultItemSchema
        ],
    ]
):
    _algo_map = {
        MfdVerificationAlgoName.MetricVerifier: MetricVerifier,
    }

    _params_schema_class = MfdVerificationTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(
        self, params: MfdVerificationTaskParams[TabularDownloadedDatasetSchema]
    ):
        dataset = params.datasets.table
        table = dataset.df

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        mfd_holds = self._algo.mfd_holds()

        if mfd_holds:
            return PrimitiveResultSchema(
                result=MfdVerificationTaskResultSchema(
                    total_count=0,
                    mfd_holds=mfd_holds,
                ),
                items=[],
            )

        clusters = self._algo.get_highlights()

        return PrimitiveResultSchema(
            result=MfdVerificationTaskResultSchema(
                total_count=len(clusters),
                mfd_holds=mfd_holds,
            ),
            items=[
                self._extract_item(
                    cluster,
                    table,
                    cluster_index,
                    params.config.lhs_indices,
                    params.config.rhs_indices,
                    params.config.parameter,
                )
                for cluster_index, cluster in enumerate(clusters)
            ],
        )

    def _extract_item(
        self,
        cluster: list[Highlight],
        table: pd.DataFrame,
        cluster_index: int,
        lhs_indices: list[int],
        rhs_indices: list[int],
        parameter: float,
    ) -> MfdVerificationTaskResultItemSchema:
        max_distance = max(highlight.max_distance for highlight in cluster)

        highlights = []
        for highlight in cluster:
            highlights.append(
                MfdVerificationHighlightSchema(
                    data_index=highlight.data_index,
                    furthest_data_index=highlight.furthest_data_index,
                    max_distance=highlight.max_distance,
                    rhs_values=[
                        str(value)
                        for value in table.iloc[highlight.data_index, rhs_indices]
                    ],
                    within_limit=highlight.max_distance <= parameter,
                )
            )

        return MfdVerificationTaskResultItemSchema(
            cluster_index=cluster_index,
            lhs_values=[
                str(value) for value in table.iloc[cluster[0].data_index, lhs_indices]
            ],
            max_distance=max_distance,
            highlights=highlights,
        )
