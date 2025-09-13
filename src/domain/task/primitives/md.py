from desbordante.md import (
    LhsSimilarityClassifierDesctription as LhsSimilarityClassifierDescription,
)
from desbordante.md import (
    MdAlgorithm,
)
from desbordante.md import (
    RhsSimilarityClassifierDesctription as RhsSimilarityClassifierDescription,
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
from pydantic import TypeAdapter

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import (
    ColumnSchema,
    PrimitiveResultSchema,
)
from src.schemas.task_schemas.primitives.md.algo_name import MdAlgoName
from src.schemas.task_schemas.primitives.md.task_params import (
    MdTaskParams,
)
from src.schemas.task_schemas.primitives.md.task_result import (
    MdSideItemSchema,
    MdTaskResultItemSchema,
    MdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.md.types import ColumnMatchMetric


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
        ColumnMatchMetric.Equality: Equality,
        ColumnMatchMetric.Jaccard: Jaccard,
        ColumnMatchMetric.Number_Difference: LVNormNumberDistance,
        ColumnMatchMetric.Date_Difference: LVNormDateDistance,
        ColumnMatchMetric.Lcs: Lcs,
        ColumnMatchMetric.Monge_Elkan: MongeElkan,
        ColumnMatchMetric.Levenshtein: Levenshtein,
    }

    _params_schema_class = MdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def _match_metrics_class_by_name(self, metrics: ColumnMatchMetric):
        if metrics_class := self._metrics_map.get(metrics):
            return metrics_class
        raise ValueError(f"Metrics {metrics} not found")

    def execute(self, params: MdTaskParams[TabularDownloadedDatasetSchema]):
        left_dataset = params.datasets.left_table
        right_dataset = params.datasets.right_table
        left_table = left_dataset.df
        right_table = right_dataset.df
        column_matches = [
            self._match_metrics_class_by_name(column_match.metric)(
                **column_match.model_dump(
                    exclude_unset=True, exclude_none=True, exclude={"metric"}
                )
            )
            for column_match in params.config.column_matches
        ]

        self._algo.load_data(left_table=left_table, right_table=right_table)

        options = self._get_algo_options(params)

        self._algo.execute(**{**options, "column_matches": column_matches})

        mds = self._algo.get_mds()

        return PrimitiveResultSchema[MdTaskResultSchema, MdTaskResultItemSchema](
            result=MdTaskResultSchema(
                total_count=len(mds),
            ),
            items=[
                MdTaskResultItemSchema(
                    lhs_items=[
                        self._extract_item(lhs) for lhs in md.get_description().lhs
                    ],
                    rhs_item=self._extract_item(md.get_description().rhs),
                )
                for md in mds
            ],
        )

    def _extract_item(
        self,
        side: LhsSimilarityClassifierDescription | RhsSimilarityClassifierDescription,
    ) -> MdSideItemSchema:
        boundary = side.decision_boundary
        metric = side.column_match_description.column_match_name
        left_column = side.column_match_description.left_column_description
        right_column = side.column_match_description.right_column_description

        return MdSideItemSchema(
            metric=TypeAdapter(ColumnMatchMetric).validate_python(metric),
            left_column=ColumnSchema(
                name=left_column.column_name,
                index=left_column.column_index,
            ),
            right_column=ColumnSchema(
                name=right_column.column_name,
                index=right_column.column_index,
            ),
            boundary=boundary,
            max_invalid_boundary=side.max_invalid_bound
            if isinstance(side, LhsSimilarityClassifierDescription)
            else None,
        )
