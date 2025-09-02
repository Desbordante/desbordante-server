from io import BytesIO

import desbordante.fd
import pandas as pd
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
from src.schemas.task_schemas.fd.algo_config import OneOfFdAlgoConfig
from src.schemas.task_schemas.fd.algo_name import FdAlgoName
from src.schemas.task_schemas.fd.task_params import FdTaskDatasetsConfig, FdTaskParams
from src.schemas.task_schemas.fd.task_result import FdModel, FdTaskResult


class FdPrimitive(
    BasePrimitive[
        desbordante.fd.FdAlgorithm,
        FdAlgoName,
        FdTaskParams,
        OneOfFdAlgoConfig,
        FdTaskDatasetsConfig[TabularDownloadedDatasetSchema],
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

    _params_schema_class = FdTaskParams
    downloaded_dataset_class = TabularDownloadedDatasetSchema
    datasets_config_class = FdTaskDatasetsConfig[TabularDownloadedDatasetSchema]

    allowed_dataset_type = DatasetType.Tabular

    def execute(
        self,
        config: OneOfFdAlgoConfig,
        datasets: FdTaskDatasetsConfig[TabularDownloadedDatasetSchema],
    ) -> FdTaskResult:
        table = datasets.table
        df = pd.read_csv(  # type: ignore
            BytesIO(table.data),
            sep=table.params.separator,
            header=0 if table.params.has_header else None,
        )
        columns = df.columns

        self._algo.load_data(table=df)  # type: ignore

        self._algo.execute(  # type: ignore
            **config.model_dump(exclude_unset=True, exclude={"algo_name"})
        )

        fds = self._algo.get_fds()  # type: ignore

        return [
            FdModel(
                lhs=[columns[index] for index in fd.lhs_indices],
                rhs=[columns[fd.rhs_index]],
            )
            for fd in fds
        ]
