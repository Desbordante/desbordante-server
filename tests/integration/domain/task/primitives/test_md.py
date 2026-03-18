import desbordante
import desbordante.md.column_matches as col_matches
import pytest

from src.domain.task.primitives.md import MdPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.md.algo_config import (
    HyMDConfig,
    LevenshteinConfig,
)
from src.schemas.task_schemas.primitives.md.algo_name import MdAlgoName
from src.schemas.task_schemas.primitives.md.task_params import (
    MdTaskDatasetsConfig,
    MdTaskParams,
)
from src.schemas.task_schemas.primitives.md.types import ColumnMatchMetric
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.domain.task.primitives.constants import ANIMALS_BEVERAGES_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
    md_to_key_from_desbordante,
    md_to_key_from_item,
)


@pytest.fixture
def animals_beverages_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(ANIMALS_BEVERAGES_CSV)


@pytest.fixture
def md_params(
    animals_beverages_dataset: TabularDownloadedDatasetSchema,
) -> MdTaskParams[TabularDownloadedDatasetSchema]:
    n_cols = animals_beverages_dataset.info.number_of_columns
    column_matches = [
        LevenshteinConfig(
            metric=ColumnMatchMetric.LEVENSHTEIN, left_column=i, right_column=i
        )
        for i in range(n_cols)
    ]
    return MdTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.MD,
        config=HyMDConfig(
            algo_name=MdAlgoName.HY_MD,
            column_matches=column_matches,  # type: ignore
        ),
        datasets=MdTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            left_table=animals_beverages_dataset,
            right_table=animals_beverages_dataset,
        ),
    )


def test_execute_returns_same_mds_as_desbordante(
    md_params: MdTaskParams[TabularDownloadedDatasetSchema],
) -> None:

    n_cols = md_params.datasets.left_table.info.number_of_columns
    column_matches = [col_matches.Levenshtein(i, i) for i in range(n_cols)]

    algo = desbordante.md.algorithms.HyMD()
    algo.load_data(
        left_table=(ANIMALS_BEVERAGES_CSV, ",", True),
        right_table=(ANIMALS_BEVERAGES_CSV, ",", True),
    )
    algo.execute(column_matches=column_matches)
    desbordante_mds = algo.get_mds()

    primitive = MdPrimitive(algo_name=MdAlgoName.HY_MD)
    primitive_result = primitive.execute(md_params)

    desbordante_keys = {md_to_key_from_desbordante(md) for md in desbordante_mds}
    primitive_keys = {
        md_to_key_from_item(item.lhs_items, item.rhs_item)
        for item in primitive_result.items
    }

    assert desbordante_keys == primitive_keys
