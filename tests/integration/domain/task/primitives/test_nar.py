import pytest
import desbordante

from src.domain.task.primitives.nar import NarPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.nar.algo_config import DesConfig
from src.schemas.task_schemas.primitives.nar.algo_name import NarAlgoName
from src.schemas.task_schemas.primitives.nar.task_params import (
    NarTaskDatasetsConfig,
    NarTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import DOG_BREEDS_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
    nar_to_key_from_desbordante,
    nar_to_key_from_item,
)

NAR_MINSUP = 0.1
NAR_MINCONF = 0.7
NAR_POPULATION_SIZE = 500
NAR_MAX_FITNESS_EVALUATIONS = 700
NAR_SEED = 5854


@pytest.fixture
def dog_breeds_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(DOG_BREEDS_CSV)


@pytest.fixture
def nar_params(
    dog_breeds_dataset: TabularDownloadedDatasetSchema,
) -> NarTaskParams[TabularDownloadedDatasetSchema]:
    return NarTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.NAR,
        config=DesConfig(
            algo_name=NarAlgoName.DES,
            minsup=NAR_MINSUP,
            minconf=NAR_MINCONF,
            population_size=NAR_POPULATION_SIZE,
            max_fitness_evaluations=NAR_MAX_FITNESS_EVALUATIONS,
            seed=NAR_SEED,
        ),
        datasets=NarTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=dog_breeds_dataset
        ),
    )


def test_execute_returns_same_nars_as_desbordante(
    nar_params: NarTaskParams[TabularDownloadedDatasetSchema],
) -> None:
    algo = desbordante.nar.algorithms.DES()
    algo.load_data(table=(DOG_BREEDS_CSV, ",", True))
    algo.execute(
        minsup=NAR_MINSUP,
        minconf=NAR_MINCONF,
        population_size=NAR_POPULATION_SIZE,
        max_fitness_evaluations=NAR_MAX_FITNESS_EVALUATIONS,
        seed=NAR_SEED,
    )
    desbordante_nars = algo.get_nars()

    primitive = NarPrimitive(algo_name=NarAlgoName.DES)
    primitive_result = primitive.execute(nar_params)

    desbordante_keys = {nar_to_key_from_desbordante(nar) for nar in desbordante_nars}
    primitive_keys = {nar_to_key_from_item(item) for item in primitive_result.items}

    assert desbordante_keys == primitive_keys
