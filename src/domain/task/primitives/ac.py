from desbordante.ac import ACException
from desbordante.ac.algorithms import AcAlgorithm as BHUNT

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.ac.algo_name import AcAlgoName
from src.schemas.task_schemas.ac.task_params import AcTaskParams
from src.schemas.task_schemas.ac.task_result import (
    AcSchema,
)


class AcPrimitive(
    BasePrimitive[
        BHUNT,
        AcAlgoName,
        AcTaskParams[TabularDownloadedDatasetSchema],
        AcSchema,
    ]
):
    _algo_map = {
        AcAlgoName.BHUNT: BHUNT,
    }

    _params_schema_class = AcTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: AcTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        column_names = dataset.info.column_names
        table = dataset.df

        self._algo.load_data(table=table)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        ac_exceptions = self._algo.get_ac_exceptions()
        ac_ranges = self._algo.get_ac_ranges()
        new_exceptions = self._extract_exceptions(ac_exceptions)

        return [
            AcSchema(
                left_column_index=range.column_indices[0],
                right_column_index=range.column_indices[1],
                left_column_name=column_names[range.column_indices[0]],
                right_column_name=column_names[range.column_indices[1]],
                ranges=range.ranges,
                exceptions=new_exceptions.setdefault(range.column_indices, []),
            )
            for range in ac_ranges
        ]

    def _extract_exceptions(self, exceptions: list[ACException]):
        columns_dict = dict()
        for ex in exceptions:
            for col in ex.column_pairs:
                if col not in columns_dict:
                    columns_dict[col] = []
                columns_dict[col].append(ex.row_index)
        return columns_dict
