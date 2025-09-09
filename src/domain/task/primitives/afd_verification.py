import pandas as pd
from desbordante.fd_verification import Highlight
from desbordante.fd_verification.algorithms import FDVerifier

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.afd_verification.algo_name import (
    AfdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.afd_verification.task_params import (
    AfdVerificationTaskParams,
)
from src.schemas.task_schemas.primitives.afd_verification.task_result import (
    AfdVerificationTaskResultItemSchema,
    AfdVerificationTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema


class AfdVerificationPrimitive(
    BasePrimitive[
        FDVerifier,
        AfdVerificationAlgoName,
        AfdVerificationTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[
            AfdVerificationTaskResultSchema,
            AfdVerificationTaskResultItemSchema,
        ],
    ]
):
    _algo_map = {
        AfdVerificationAlgoName.FDVerifier: FDVerifier,
    }

    _params_schema_class = AfdVerificationTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(
        self, params: AfdVerificationTaskParams[TabularDownloadedDatasetSchema]
    ):
        dataset = params.datasets.table
        table = dataset.df

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        clusters = [
            self._extract_cluster(highlight, table)
            for highlight in self._algo.get_highlights()
        ]

        return PrimitiveResultSchema(
            result=AfdVerificationTaskResultSchema(
                total_count=len(clusters),
                error=self._algo.get_error(),
                num_error_clusters=self._algo.get_num_error_clusters(),
                num_error_rows=self._algo.get_num_error_rows(),
            ),
            items=clusters,
        )

    def _extract_cluster(
        self, highlight: Highlight, table: pd.DataFrame
    ) -> AfdVerificationTaskResultItemSchema:
        return AfdVerificationTaskResultItemSchema(
            num_distinct_rhs_values=highlight.num_distinct_rhs_values,
            most_frequent_rhs_value_proportion=highlight.most_frequent_rhs_value_proportion,
            rows=[
                [str(table.iloc[index][j]) for j in table.columns]
                for index in highlight.cluster
            ],
        )
