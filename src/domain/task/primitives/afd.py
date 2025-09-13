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
        column_names = dataset.info.column_names

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
                    lhs_indices=fd.lhs_indices,
                    lhs_columns=[column_names[index] for index in fd.lhs_indices],
                    rhs_index=fd.rhs_index,
                    rhs_column=column_names[fd.rhs_index],
                )
                for fd in fds
            ],
        )
