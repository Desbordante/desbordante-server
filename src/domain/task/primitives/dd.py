import re

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
        column_names = dataset.info.column_names

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options, difference_table=difference_table)

        dds = self._algo.get_dds()

        return PrimitiveResultSchema[DdTaskResultSchema, DdTaskResultItemSchema](
            result=DdTaskResultSchema(
                total_count=len(dds),
            ),
            items=[self._extract_item(str(dd), column_names) for dd in dds],
        )

    def _extract_item(self, dd: str, column_names: list[str]) -> DdTaskResultItemSchema:
        pattern = r"^(.+?)\s*->\s*(.+?)$"
        match = re.match(pattern, dd.strip())

        if not match:
            raise ValueError(f"Invalid DD format: {dd}")

        lhs_part, rhs_part = match.groups()

        item_pattern = r"(\w+)\s*\[(\d+),\s*(\d+)\]"

        lhs_items = [
            DdSideItemSchema(
                column_name=name,
                column_index=column_names.index(name),
                distance_interval=(int(start), int(end)),
            )
            for name, start, end in re.findall(item_pattern, lhs_part)
        ]

        rhs_match = re.search(item_pattern, rhs_part)
        if not rhs_match:
            raise ValueError(f"Invalid DD right part format: {rhs_part}")

        rhs_name, rhs_start, rhs_end = rhs_match.groups()
        rhs_item = DdSideItemSchema(
            column_name=rhs_name,
            column_index=column_names.index(rhs_name),
            distance_interval=(int(rhs_start), int(rhs_end)),
        )

        return DdTaskResultItemSchema(lhs_items=lhs_items, rhs_item=rhs_item)
