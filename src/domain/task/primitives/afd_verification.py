from dataclasses import dataclass

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
    AfdVerificationRowSchema,
    AfdVerificationTaskResultItemSchema,
    AfdVerificationTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema


@dataclass
class AfdVerificationResult:
    items: list[AfdVerificationTaskResultItemSchema]
    min_num: int | None
    max_num: int | None
    min_prop: float | None
    max_prop: float | None


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

        highlights = self._algo.get_highlights()
        result = self._extract_result(
            highlights,
            table,
        )

        return PrimitiveResultSchema(
            result=AfdVerificationTaskResultSchema(
                total_count=len(result.items),
                afd_holds=self._algo.fd_holds(),
                error=self._algo.get_error(),
                number_of_error_clusters=self._algo.get_num_error_clusters(),
                number_of_error_rows=self._algo.get_num_error_rows(),
                min_number_of_distinct_rhs_values=result.min_num,
                max_number_of_distinct_rhs_values=result.max_num,
                min_most_frequent_rhs_value_proportion=result.min_prop,
                max_most_frequent_rhs_value_proportion=result.max_prop,
            ),
            items=result.items,
        )

    def _extract_result(
        self,
        highlights: list[Highlight],
        table: pd.DataFrame,
    ) -> AfdVerificationResult:
        items = [self._create_item(highlight, table) for highlight in highlights]
        distinct_rhs_values = [h.num_distinct_rhs_values for h in highlights]
        proportions = [h.most_frequent_rhs_value_proportion for h in highlights]

        return AfdVerificationResult(
            items=items,
            min_num=min(distinct_rhs_values) if distinct_rhs_values else None,
            max_num=max(distinct_rhs_values) if distinct_rhs_values else None,
            min_prop=min(proportions) if proportions else None,
            max_prop=max(proportions) if proportions else None,
        )

    def _create_item(
        self, highlight: Highlight, table: pd.DataFrame
    ) -> AfdVerificationTaskResultItemSchema:
        return AfdVerificationTaskResultItemSchema(
            number_of_distinct_rhs_values=highlight.num_distinct_rhs_values,
            most_frequent_rhs_value_proportion=highlight.most_frequent_rhs_value_proportion,
            rows=[
                AfdVerificationRowSchema(
                    row_index=index,
                    values=[str(value) for value in table.iloc[index]],
                )
                for index in highlight.cluster
            ],
        )
