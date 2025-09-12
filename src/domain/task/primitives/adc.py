import re

from desbordante.dc.algorithms import FastADC
from pydantic import TypeAdapter

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.adc.algo_name import AdcAlgoName
from src.schemas.task_schemas.primitives.adc.task_params import AdcTaskParams
from src.schemas.task_schemas.primitives.adc.task_result import (
    AdcItemSchema,
    AdcTaskResultItemSchema,
    AdcTaskResultSchema,
)
from src.schemas.task_schemas.primitives.adc.types import Operator
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema


class AdcPrimitive(
    BasePrimitive[
        FastADC,
        AdcAlgoName,
        AdcTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[AdcTaskResultSchema, AdcTaskResultItemSchema],
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

        dcs = self._algo.get_dcs()

        return PrimitiveResultSchema[AdcTaskResultSchema, AdcTaskResultItemSchema](
            result=AdcTaskResultSchema(
                total_count=len(dcs),
            ),
            items=[self._extract_result(str(dc)) for dc in dcs],
        )

    def _extract_result(self, dc: str) -> AdcTaskResultItemSchema:
        dc_clean = re.sub(r"^¬\{\s*|\s*\}$", "", dc.strip())
        conjuncts = re.split(r"\s*∧\s*", dc_clean)

        cojuncts = []
        left_columns = set()
        right_columns = set()
        for conjunct in conjuncts:
            match = re.match(
                r"([ts])\.(\w+)\s*(<=|>=|<|>|==|!=)\s*([ts])\.(\w+)", conjunct.strip()
            )

            if not match:
                continue

            left_prefix, left_column, operator, right_prefix, right_column = (
                match.groups()
            )

            cojuncts.append(
                AdcItemSchema(
                    left_prefix=left_prefix,
                    left_column=left_column,
                    right_prefix=right_prefix,
                    right_column=right_column,
                    operator=TypeAdapter(Operator).validate_python(operator),
                )
            )
            left_columns.add(left_column)
            right_columns.add(right_column)

        return AdcTaskResultItemSchema(
            cojuncts=cojuncts,
            left_columns=sorted(left_columns),
            right_columns=sorted(right_columns),
        )
