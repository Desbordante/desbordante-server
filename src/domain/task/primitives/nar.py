from desbordante.nar.algorithms import DES

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.nar.algo_name import NarAlgoName
from src.schemas.task_schemas.primitives.nar.task_params import (
    NarTaskParams,
)
from src.schemas.task_schemas.primitives.nar.task_result import (
    NarSideItemSchema,
    NarTaskResultItemSchema,
    NarTaskResultSchema,
)


class NarPrimitive(
    BasePrimitive[
        DES,
        NarAlgoName,
        NarTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[NarTaskResultSchema, NarTaskResultItemSchema],
    ]
):
    _algo_map = {
        NarAlgoName.DES: DES,
    }

    _params_schema_class = NarTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: NarTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        table = dataset.df
        columns = dataset.info.column_names

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        return PrimitiveResultSchema[NarTaskResultSchema, NarTaskResultItemSchema](
            result=NarTaskResultSchema(
                total_count=len(self._algo.get_nars()),
            ),
            items=[
                NarTaskResultItemSchema(
                    confidence=nar.confidence,
                    support=nar.support,
                    lhs=self._extract_side(nar.ante.items(), columns),
                    rhs=self._extract_side(nar.cons.items(), columns),
                )
                for nar in self._algo.get_nars()
            ],
        )

    def _extract_side(self, side, columns) -> list[NarSideItemSchema]:
        return [
            NarSideItemSchema(name=columns[column_index], values=str(value))
            for column_index, value in side
        ]
