import pytest
import desbordante

from src.domain.task.primitives.fd import FdPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.fd.algo_config import HyFDConfig
from src.schemas.task_schemas.primitives.fd.algo_name import FdAlgoName
from src.schemas.task_schemas.primitives.fd.task_params import (
    FdTaskDatasetsConfig,
    FdTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import UNIVERSITY_FD_CSV
from tests.integration.domain.task.primitives.helpers import (
    fd_to_key,
    load_tabular_dataset_from_csv,
)


@pytest.fixture
def university_fd_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(UNIVERSITY_FD_CSV)


@pytest.fixture
def fd_params(
    university_fd_dataset: TabularDownloadedDatasetSchema,
) -> FdTaskParams[TabularDownloadedDatasetSchema]:
    return FdTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.FD,
        config=HyFDConfig(algo_name=FdAlgoName.HY_FD),
        datasets=FdTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=university_fd_dataset
        ),
    )


def test_execute_returns_same_fds_as_desbordante(
    fd_params: FdTaskParams[TabularDownloadedDatasetSchema],
) -> None:
    algo = desbordante.fd.algorithms.HyFD()
    algo.load_data(table=(UNIVERSITY_FD_CSV, ",", True))
    algo.execute()
    desbordante_fds = algo.get_fds()

    primitive = FdPrimitive(algo_name=FdAlgoName.HY_FD)
    primitive_result = primitive.execute(fd_params)

    desbordante_keys = {
        fd_to_key(tuple(fd.lhs_indices), fd.rhs_index) for fd in desbordante_fds
    }
    primitive_keys = {
        fd_to_key(
            tuple(col.index for col in item.lhs_columns),
            item.rhs_column.index,
        )
        for item in primitive_result.items
    }

    assert desbordante_keys == primitive_keys
