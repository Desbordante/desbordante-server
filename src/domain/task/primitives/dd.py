from desbordante.dd.algorithms import Split

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import (
    DatasetType,
    TabularDownloadedDatasetSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.dd.algo_name import DdAlgoName
from src.schemas.task_schemas.primitives.dd.task_params import (
    DdTaskParams,
)
from src.schemas.task_schemas.primitives.dd.task_result import (
    DdSideItemSchema,
    DdTaskResultItemSchema,
    DdTaskResultSchema,
)


class DdPrimitive(
    BasePrimitive[
        Split,
        DdAlgoName,
        DdTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[DdTaskResultSchema, DdTaskResultItemSchema],
    ]
):
    _algo_map = {
        DdAlgoName.Split: Split,
    }

    _params_schema_class = DdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: DdTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        table = dataset.df
        difference_table = params.datasets.dif_table.df

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options, difference_table=difference_table)

        return PrimitiveResultSchema[DdTaskResultSchema, DdTaskResultItemSchema](
            result=DdTaskResultSchema(
                total_count=len(self._algo.get_dds()),
            ),
            items=[self._split_result(str(dd)) for dd in self._algo.get_dds()],
        )

    def _split_side(self, raw: list[str]) -> list[DdSideItemSchema]:
        ans = []
        for s in raw:
            name, value = s.split(" [")
            value = "[" + value
            ans.append(DdSideItemSchema(name=name, values=value))
        return ans

    def _split_result(self, row: str) -> DdTaskResultItemSchema:
        lhs_rawraw, rhs_raw = row.split(" -> ")
        lhs_raw = lhs_rawraw.split(" ; ")
        lhs_ans = self._split_side(lhs_raw)
        rhs_ans = self._split_side([rhs_raw])
        return DdTaskResultItemSchema(lhs=lhs_ans, rhs=rhs_ans)
