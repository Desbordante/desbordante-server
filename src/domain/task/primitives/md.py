from typing import Sequence

from desbordante.md import (
    LhsSimilarityClassifierDesctription,
    MdAlgorithm,
    RhsSimilarityClassifierDesctription,
)
from desbordante.md.algorithms import HyMD
from desbordante.md.column_matches import (
    Equality,
    Jaccard,
    Lcs,
    Levenshtein,
    LVNormDateDistance,
    LVNormNumberDistance,
    MongeElkan,
)

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.md.algo_name import MdAlgoName
from src.schemas.task_schemas.primitives.md.task_params import (
    MdTaskParams,
)
from src.schemas.task_schemas.primitives.md.task_result import (
    MdSideItemSchema,
    MdTaskResultItemSchema,
    MdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.md.types import ColumnMatchMetrics


class MdPrimitive(
    BasePrimitive[
        MdAlgorithm,
        MdAlgoName,
        MdTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[MdTaskResultSchema, MdTaskResultItemSchema],
    ]
):
    _algo_map = {
        MdAlgoName.HyMD: HyMD,
    }

    _metrics_map = {
        ColumnMatchMetrics.Equality: Equality,
        ColumnMatchMetrics.Jaccard: Jaccard,
        ColumnMatchMetrics.Number_Difference: LVNormNumberDistance,
        ColumnMatchMetrics.Date_Difference: LVNormDateDistance,
        ColumnMatchMetrics.Lcs: Lcs,
        ColumnMatchMetrics.Monge_Elkan: MongeElkan,
        ColumnMatchMetrics.Levenshtein: Levenshtein,
    }

    _params_schema_class = MdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def _match_metrics_class_by_name(self, metrics: ColumnMatchMetrics):
        if metrics_class := self._metrics_map.get(metrics):
            return metrics_class
        raise ValueError(f"Metrics {metrics} not found")

    def execute(self, params: MdTaskParams[TabularDownloadedDatasetSchema]):
        left_dataset = params.datasets.left_table
        right_dataset = params.datasets.right_table
        left_table = left_dataset.df
        right_table = right_dataset.df
        column_matches = [
            self._match_metrics_class_by_name(metric.metrics)(
                **metric.model_dump(exclude_unset=True, exclude={"metrics"})
            )
            for metric in params.config.column_matches
        ]

        self._algo.load_data(left_table=left_table, right_table=right_table)

        options = self._get_algo_options(params)

        self._algo.execute(**{**options, "column_matches": column_matches})

        return PrimitiveResultSchema[MdTaskResultSchema, MdTaskResultItemSchema](
            result=MdTaskResultSchema(
                total_count=len(self._algo.get_mds()),
            ),
            items=[
                MdTaskResultItemSchema(
                    lhs=self._extract_side(md.get_description().lhs),
                    rhs=self._extract_side([md.get_description().rhs]),
                )
                for md in self._algo.get_mds()
            ],
        )

    def _extract_side(
        self,
        side: Sequence[
            LhsSimilarityClassifierDesctription | RhsSimilarityClassifierDesctription
        ],
    ) -> list[MdSideItemSchema]:
        sides = []
        for s in side:
            boundary = s.decision_boundary
            metrics = s.column_match_description.column_match_name
            column1 = s.column_match_description.left_column_description.column_name
            column2 = s.column_match_description.right_column_description.column_name
            sides.append(
                MdSideItemSchema(
                    metrics=metrics,
                    left_column=column1,
                    right_column=column2,
                    boundary=boundary,
                )
            )
        return sides
