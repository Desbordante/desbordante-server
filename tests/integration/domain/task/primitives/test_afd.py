import pytest
import desbordante

from src.domain.task.primitives.afd import AfdPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.afd.algo_config import (
    AFDPyroConfig,
    AFDTaneConfig,
)
from src.schemas.task_schemas.primitives.afd.algo_name import AfdAlgoName
from src.schemas.task_schemas.primitives.afd.task_params import (
    AfdTaskDatasetsConfig,
    AfdTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import INVENTORY_AFD_CSV
from tests.integration.domain.task.primitives.helpers import (
    fd_to_key,
    load_tabular_dataset_from_csv,
)

AFD_ERROR = 0.3
AFD_ERROR_MEASURES = ["g1", "pdep", "tau", "mu_plus", "rho"]


@pytest.fixture
def inventory_afd_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(INVENTORY_AFD_CSV)


@pytest.fixture
def afd_pyro_params(
    inventory_afd_dataset: TabularDownloadedDatasetSchema,
) -> AfdTaskParams[TabularDownloadedDatasetSchema]:
    return AfdTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.AFD,
        config=AFDPyroConfig(algo_name=AfdAlgoName.PYRO, error=AFD_ERROR),
        datasets=AfdTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=inventory_afd_dataset
        ),
    )


def test_execute_returns_same_afds_as_desbordante_pyro(
    afd_pyro_params: AfdTaskParams[TabularDownloadedDatasetSchema],
) -> None:
    algo = desbordante.afd.algorithms.Pyro()
    algo.load_data(table=(INVENTORY_AFD_CSV, ",", True))
    algo.execute(error=AFD_ERROR)
    desbordante_fds = algo.get_fds()

    primitive = AfdPrimitive(algo_name=AfdAlgoName.PYRO)
    primitive_result = primitive.execute(afd_pyro_params)

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


@pytest.mark.parametrize("afd_error_measure", AFD_ERROR_MEASURES)
def test_execute_returns_same_afds_as_desbordante_tane(
    inventory_afd_dataset: TabularDownloadedDatasetSchema,
    afd_error_measure: str,
) -> None:
    algo = desbordante.afd.algorithms.Tane()
    algo.load_data(table=(INVENTORY_AFD_CSV, ",", True))
    algo.execute(error=AFD_ERROR, afd_error_measure=afd_error_measure)
    desbordante_fds = algo.get_fds()

    params = AfdTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.AFD,
        config=AFDTaneConfig(
            algo_name=AfdAlgoName.TANE,
            error=AFD_ERROR,
            afd_error_measure=afd_error_measure,  # type: ignore
        ),
        datasets=AfdTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=inventory_afd_dataset
        ),
    )

    primitive = AfdPrimitive(algo_name=AfdAlgoName.TANE)
    primitive_result = primitive.execute(params)

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
