import desbordante.fd
from desbordante.afd.algorithms import (
    Pyro,
    Tane,
)

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.afd.algo_name import AfdAlgoName
from src.schemas.task_schemas.primitives.afd.task_params import AfdTaskParams
from src.schemas.task_schemas.primitives.afd.task_result import (
    AfdTaskResultItemSchema,
    AfdTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema


class AfdPrimitive(
    BasePrimitive[
        desbordante.fd.FdAlgorithm,
        AfdAlgoName,
        AfdTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[AfdTaskResultSchema, AfdTaskResultItemSchema],
    ]
):
    _algo_map = {
        AfdAlgoName.Pyro: Pyro,
        AfdAlgoName.Tane: Tane,
    }

    _params_schema_class = AfdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: AfdTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table
        columns = dataset.info.column_names

        self._algo.load_data(table=dataset.df)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        fds = self._algo.get_fds()

        return PrimitiveResultSchema(
            result=AfdTaskResultSchema(
                total_count=len(fds),
            ),
            items=[
                AfdTaskResultItemSchema(
                    left_indices=fd.lhs_indices,
                    left_columns=[columns[index] for index in fd.lhs_indices],
                    right_index=fd.rhs_index,
                    right_column=columns[fd.rhs_index],
                )
                for fd in fds
            ],
        )
