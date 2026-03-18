import pytest
import desbordante

from src.domain.task.primitives.pfd import PfdPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.pfd.algo_config import PfdTaneConfig
from src.schemas.task_schemas.primitives.pfd.algo_name import PfdAlgoName
from src.schemas.task_schemas.primitives.pfd.task_params import (
    PfdTaskDatasetsConfig,
    PfdTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import PFD_CSV
from tests.integration.domain.task.primitives.helpers import (
    fd_to_key,
    load_tabular_dataset_from_csv,
)

PFD_ERROR = 0.02777777778
PFD_ERROR_MEASURE = "per_value"


@pytest.fixture
def pfd_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(PFD_CSV)


@pytest.fixture
def pfd_params(
    pfd_dataset: TabularDownloadedDatasetSchema,
) -> PfdTaskParams[TabularDownloadedDatasetSchema]:
    return PfdTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.PFD,
        config=PfdTaneConfig(
            algo_name=PfdAlgoName.PFD_TANE,
            error=PFD_ERROR,
            pfd_error_measure=PFD_ERROR_MEASURE,
        ),
        datasets=PfdTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=pfd_dataset
        ),
    )


def test_execute_returns_same_pfds_as_desbordante(
    pfd_params: PfdTaskParams[TabularDownloadedDatasetSchema],
) -> None:
    algo = desbordante.pfd.algorithms.PFDTane()
    algo.load_data(table=(PFD_CSV, ",", True))
    algo.execute(error=PFD_ERROR, pfd_error_measure=PFD_ERROR_MEASURE)
    desbordante_fds = algo.get_fds()

    primitive = PfdPrimitive(algo_name=PfdAlgoName.PFD_TANE)
    primitive_result = primitive.execute(pfd_params)

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
