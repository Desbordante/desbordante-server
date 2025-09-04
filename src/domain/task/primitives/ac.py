from desbordante.ac.algorithms import AcAlgorithm as BHUNT

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.ac.algo_name import AcAlgoName
from src.schemas.task_schemas.ac.task_params import AcTaskParams
from src.schemas.task_schemas.ac.task_result import (
    AcExceptionSchema,
    AcRangesSchema,
    AcResultType,
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

        self._algo.load_data(table=table)  # type: ignore

        self._algo.execute(  # type: ignore
            **params.config.model_dump(
                exclude_unset=True, exclude={"algo_name", "column_indices"}
            )
        )

        ac_exceptions = self._algo.get_ac_exceptions()  # type: ignore
        ac_ranges = self._algo.get_ac_ranges()  # type: ignore

        return [
            AcRangesSchema(
                type=AcResultType.Range,
                left_column_index=range.column_indices[0],
                right_column_index=range.column_indices[1],
                left_column_name=column_names[range.column_indices[0]],
                right_column_name=column_names[range.column_indices[1]],
                ranges=range.ranges,
            )
            for range in ac_ranges
        ] + [
            AcExceptionSchema(
                type=AcResultType.Exception,
                column_pairs=exception.column_pairs,
                column_pairs_names=[
                    (column_names[pair[0]], column_names[pair[1]])
                    for pair in exception.column_pairs
                ],
                row_index=exception.row_index,
            )
            for exception in ac_exceptions
        ]
