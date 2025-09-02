import desbordante.fd
from desbordante.fd.algorithms import (
    DFD,
    FUN,
    Aid,
    Depminer,
    FastFDs,
    FDep,
    FdMine,
    HyFD,
    Pyro,
    Tane,
)

from src.domain.task.primitives.base_primitive import BasePrimitive
from src.schemas.dataset_schemas import DatasetType, TabularDownloadedDatasetSchema
from src.schemas.task_schemas.fd.algo_name import FdAlgoName
from src.schemas.task_schemas.fd.task_params import FdTaskParams
from src.schemas.task_schemas.fd.task_result import FdSchema, FdTaskResult
from src.schemas.task_schemas.types import PrimitiveName


class FdPrimitive(
    BasePrimitive[
        desbordante.fd.FdAlgorithm,
        FdAlgoName,
        FdTaskParams[TabularDownloadedDatasetSchema],
        FdTaskResult,
    ]
):
    _algo_map = {
        FdAlgoName.Aid: Aid,
        FdAlgoName.DFD: DFD,
        FdAlgoName.Depminer: Depminer,
        FdAlgoName.FDep: FDep,
        FdAlgoName.FUN: FUN,
        FdAlgoName.FastFDs: FastFDs,
        FdAlgoName.FdMine: FdMine,
        FdAlgoName.HyFD: HyFD,
        FdAlgoName.Pyro: Pyro,
        FdAlgoName.Tane: Tane,
    }

    _params_schema_class = FdTaskParams[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(self, params: FdTaskParams[TabularDownloadedDatasetSchema]):
        dataset = params.datasets.table

        self._algo.load_data(table=dataset.df)  # type: ignore

        self._algo.execute(  # type: ignore
            **params.config.model_dump(exclude_unset=True, exclude={"algo_name"})
        )

        fds = self._algo.get_fds()  # type: ignore

        return FdTaskResult(
            primitive_name=PrimitiveName.FD,
            result=[
                FdSchema(lhs_indices=fd.lhs_indices, rhs_index=fd.rhs_index)
                for fd in fds
            ],
            total_count=len(fds),
        )
