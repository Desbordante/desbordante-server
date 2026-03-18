import pytest
import desbordante

from src.domain.task.primitives.dd import DdPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.dd.algo_config import SplitConfig
from src.schemas.task_schemas.primitives.dd.algo_name import DdAlgoName
from src.schemas.task_schemas.primitives.dd.task_params import (
    DdTaskDatasetsConfig,
    DdTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import (
    FLIGHTS_DD_CSV,
    FLIGHTS_DD_DIF_TABLE_CSV,
)
from tests.integration.domain.task.primitives.helpers import (
    dd_to_key_from_item,
    dd_to_key_from_string,
    load_tabular_dataset_from_csv,
)


@pytest.fixture
def flights_dd_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(FLIGHTS_DD_CSV)


@pytest.fixture
def flights_dd_dif_table_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(FLIGHTS_DD_DIF_TABLE_CSV)


@pytest.fixture
def dd_params(
    flights_dd_dataset: TabularDownloadedDatasetSchema,
    flights_dd_dif_table_dataset: TabularDownloadedDatasetSchema,
) -> DdTaskParams[TabularDownloadedDatasetSchema]:
    return DdTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.DD,
        config=SplitConfig(algo_name=DdAlgoName.SPLIT),
        datasets=DdTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=flights_dd_dataset,
            dif_table=flights_dd_dif_table_dataset,
        ),
    )


def test_execute_returns_same_dds_as_desbordante(
    dd_params: DdTaskParams[TabularDownloadedDatasetSchema],
) -> None:
    algo = desbordante.dd.algorithms.Split()
    algo.load_data(table=(FLIGHTS_DD_CSV, ",", True))
    algo.execute(difference_table=(FLIGHTS_DD_DIF_TABLE_CSV, ",", True))
    desbordante_dds = algo.get_dds()

    primitive = DdPrimitive(algo_name=DdAlgoName.SPLIT)
    primitive_result = primitive.execute(dd_params)

    desbordante_keys = {dd_to_key_from_string(str(dd)) for dd in desbordante_dds}
    primitive_keys = {
        dd_to_key_from_item(item.lhs_items, item.rhs_item)
        for item in primitive_result.items
    }

    assert desbordante_keys == primitive_keys
