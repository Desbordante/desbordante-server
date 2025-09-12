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
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.schemas.task_schemas.primitives.fd.algo_name import FdAlgoName
from src.schemas.task_schemas.primitives.fd.task_params import FdTaskParams
from src.schemas.task_schemas.primitives.fd.task_result import (
    FdTaskResultItemSchema,
    FdTaskResultSchema,
)


class FdPrimitive(
    BasePrimitive[
        desbordante.fd.FdAlgorithm,
        FdAlgoName,
        FdTaskParams[TabularDownloadedDatasetSchema],
        PrimitiveResultSchema[FdTaskResultSchema, FdTaskResultItemSchema],
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
        columns = dataset.info.column_names

        self._algo.load_data(table=dataset.df)

        options = self._get_algo_options(params)

        self._algo.execute(**options)

        fds = self._algo.get_fds()

        return PrimitiveResultSchema(
            result=FdTaskResultSchema(
                total_count=len(fds),
            ),
            items=[
                FdTaskResultItemSchema(
                    left_indices=fd.lhs_indices,
                    left_columns=[columns[index] for index in fd.lhs_indices],
                    right_index=fd.rhs_index,
                    right_column=columns[fd.rhs_index],
                )
                for fd in fds
            ],
        )
