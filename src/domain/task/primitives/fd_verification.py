from dataclasses import dataclass

import pandas as pd
from desbordante.fd_verification import Highlight
from desbordante.fd_verification.algorithms import FDVerifier as FdVerifier

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.fd_verification.algo_name import (
    FdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.fd_verification.task_params import (
    FdVerificationTaskParams,
)
from src.schemas.task_schemas.primitives.fd_verification.task_result import (
    FdVerificationRowSchema,
    FdVerificationTaskResultItemSchema,
    FdVerificationTaskResultSchema,
    HoldsFdVerificationTaskResultSchema,
    NotHoldsFdVerificationTaskResultSchema,
)


@dataclass
class FdVerificationResult:
    items: list[FdVerificationTaskResultItemSchema]
    min_num: int
    max_num: int
    min_prop: float
    max_prop: float


class FdVerificationPrimitive(
    BasePrimitive[
        FdVerifier,
        FdVerificationAlgoName,
        FdVerificationTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[
            FdVerificationTaskResultSchema,
            FdVerificationTaskResultItemSchema,
        ],
    ]
):
    _algo_map = {
        FdVerificationAlgoName.FdVerifier: FdVerifier,
    }

    _params_schema_class = FdVerificationTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(
        self, params: FdVerificationTaskParams[TabularDownloadedDatasetSchema]
    ) -> PrimitiveResultSchema[
        FdVerificationTaskResultSchema,
        FdVerificationTaskResultItemSchema,
    ]:
        dataset = params.datasets.table
        table = dataset.df

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        fd_holds = self._algo.fd_holds()

        if fd_holds:
            return PrimitiveResultSchema(
                result=HoldsFdVerificationTaskResultSchema(
                    total_count=0,
                    fd_holds=fd_holds,
                    error=0,
                    number_of_error_clusters=0,
                    number_of_error_rows=0,
                ),
                items=[],
            )

        highlights = self._algo.get_highlights()
        result = self._extract_result(
            highlights,
            table,
        )

        return PrimitiveResultSchema(
            result=NotHoldsFdVerificationTaskResultSchema(
                total_count=len(result.items),
                fd_holds=fd_holds,
                error=self._algo.get_error(),
                number_of_error_clusters=self._algo.get_num_error_clusters(),
                number_of_error_rows=self._algo.get_num_error_rows(),
                min_num=result.min_num,
                max_num=result.max_num,
                min_prop=result.min_prop,
                max_prop=result.max_prop,
            ),
            items=result.items,
        )

    def _extract_result(
        self,
        highlights: list[Highlight],
        table: pd.DataFrame,
    ) -> FdVerificationResult:
        items = [self._create_item(highlight, table) for highlight in highlights]
        distinct_rhs_values = [h.num_distinct_rhs_values for h in highlights]
        proportions = [h.most_frequent_rhs_value_proportion for h in highlights]

        return FdVerificationResult(
            items=items,
            min_num=min(distinct_rhs_values),
            max_num=max(distinct_rhs_values),
            min_prop=min(proportions),
            max_prop=max(proportions),
        )

    def _create_item(
        self, highlight: Highlight, table: pd.DataFrame
    ) -> FdVerificationTaskResultItemSchema:
        return FdVerificationTaskResultItemSchema(
            number_of_distinct_rhs_values=highlight.num_distinct_rhs_values,
            most_frequent_rhs_value_proportion=highlight.most_frequent_rhs_value_proportion,
            rows=[
                FdVerificationRowSchema(
                    row_index=index,
                    values=[str(value) for value in table.iloc[index]],
                )
                for index in highlight.cluster
            ],
        )
