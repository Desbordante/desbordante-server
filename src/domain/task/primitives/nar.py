from desbordante.nar import (
    FloatValueRange,
    IntValueRange,
    StringValueRange,
    ValueRange,
)
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
    NarFloatSideItemSchema,
    NarIntegerSideItemSchema,
    NarSideItemSchema,
    NarStringSideItemSchema,
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
        column_names = dataset.info.column_names

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        nars = self._algo.get_nars()

        return PrimitiveResultSchema[NarTaskResultSchema, NarTaskResultItemSchema](
            result=NarTaskResultSchema(
                total_count=len(nars),
            ),
            items=[
                NarTaskResultItemSchema(
                    confidence=nar.confidence,
                    support=nar.support,
                    fitness=nar.fitness,
                    lhs_items=self._extract_side(nar.ante, column_names),
                    rhs_items=self._extract_side(nar.cons, column_names),
                )
                for nar in nars
            ],
        )

    def _extract_side(
        self, side: dict[int, ValueRange], column_names: list[str]
    ) -> list[NarSideItemSchema]:
        items = []
        for column_index, value in side.items():
            if isinstance(value, StringValueRange):
                items.append(
                    NarStringSideItemSchema(
                        type="string",
                        name=column_names[column_index],
                        index=column_index,
                        values=value.string,
                    )
                )
            elif isinstance(value, IntValueRange):
                items.append(
                    NarIntegerSideItemSchema(
                        type="integer",
                        name=column_names[column_index],
                        index=column_index,
                        range=(value.lower_bound, value.upper_bound),
                    )
                )
            elif isinstance(value, FloatValueRange):
                items.append(
                    NarFloatSideItemSchema(
                        type="float",
                        name=column_names[column_index],
                        index=column_index,
                        range=(value.lower_bound, value.upper_bound),
                    )
                )
            else:
                raise ValueError(f"Invalid value type: {type(value)}")
        return items
