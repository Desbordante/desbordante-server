from desbordante.dc.algorithms import FastADC

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.adc.algo_name import AdcAlgoName
from src.schemas.task_schemas.adc.task_params import AdcTaskParams
from src.schemas.task_schemas.adc.task_result import (
    AdcItemSchema,
    AdcSchema,
)


class AdcPrimitive(
    BasePrimitive[
        FastADC,
        AdcAlgoName,
        AdcTaskParams[TabularDownloadedDatasetSchema],
        AdcSchema,
    ]
):
    _algo_map = {
        AdcAlgoName.FastADC: FastADC,
    }

    _params_schema_class = AdcTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: AdcTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        table = dataset.df

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        return [
            AdcSchema(cojuncts=self._split_result(str(dc)))
            for dc in self._algo.get_dcs()
        ]

    def _split_result(self, row: str) -> list[AdcItemSchema]:
        row_len = len(row)
        row = row[2 : row_len - 1]
        conjuncts = row.split("∧")
        result = []
        for con in conjuncts:
            left_item, sign, right_item = con.split()
            result.append(
                AdcItemSchema(left_item=left_item, sign=sign, right_item=right_item)  # type: ignore
            )
        return result
