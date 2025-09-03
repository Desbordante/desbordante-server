import desbordante.afd
import desbordante.fd
from desbordante.afd.algorithms import (
    Pyro,
    Tane,
)

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.afd.algo_name import AfdAlgoName
from src.schemas.task_schemas.afd.task_params import AfdTaskParams
from src.schemas.task_schemas.afd.task_result import AfdSchema


class AfdPrimitive(
    BasePrimitive[
        desbordante.fd.FdAlgorithm,
        AfdAlgoName,
        AfdTaskParams[TabularDownloadedDatasetSchema],
        AfdSchema,
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

        self._algo.load_data(table=dataset.df)  # type: ignore

        self._algo.execute(  # type: ignore
            **params.config.model_dump(exclude_unset=True, exclude={"algo_name"})
        )

        fds = self._algo.get_fds()  # type: ignore

        return [
            AfdSchema(
                lhs_indices=fd.lhs_indices,
                lhs_names=[columns[index] for index in fd.lhs_indices],
                rhs_index=fd.rhs_index,
                rhs_name=columns[fd.rhs_index],
            )
            for fd in fds
        ]
