from operator import attrgetter

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
    HighlightSchema,
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

        if self._algo.mfd_holds():
            return PrimitiveResultSchema(
                result=MfdVerificationTaskResultSchema(
                    total_count=0,
                    mfd_holds=True,
                ),
                items=[],
            )
        else:
            hidhlights_clusters: list[MfdVerificationTaskResultItemSchema] = []
            highlights_list = self._algo.get_highlights()
            for cluster_index, cluster in enumerate(highlights_list):
                # get lhs values of the first row of the cluster
                cluster_name = (
                    list(
                        map(
                            str,
                            table.iloc[
                                [cluster[0].data_index],
                                params.config.lhs_indices,
                            ].values[0],
                        )
                    )
                    if len(cluster) > 0
                    else []
                )
                max_distance = max(map(attrgetter("max_distance"), cluster))
                highlights: list[HighlightSchema] = []
                for highlight_index, highlight in enumerate(cluster):
                    # get rhs values of the current row in the cluster
                    value = (
                        list(
                            map(
                                str,
                                table.iloc[
                                    [highlight.data_index],
                                    params.config.rhs_indices,
                                ].values[0],
                            )
                        )
                        if len(cluster) > 0
                        else []
                    )
                    highlights.append(
                        HighlightSchema(
                            highlight_index=highlight_index,
                            data_index=highlight.data_index,
                            furthest_data_index=highlight.furthest_data_index,
                            max_distance=highlight.max_distance,
                            within_limit=highlight.max_distance
                            <= params.config.parameter,
                            value=value,
                        )
                    )
                hidhlights_clusters.append(
                    MfdVerificationTaskResultItemSchema(
                        cluster_index=cluster_index,
                        cluster_name=cluster_name,
                        max_distance=max_distance,
                        highlights_count=len(highlights),
                        highlights=highlights,
                    )
                )

            return PrimitiveResultSchema(
                result=MfdVerificationTaskResultSchema(
                    total_count=len(hidhlights_clusters),
                    mfd_holds=False,
                ),
                items=hidhlights_clusters,
            )
