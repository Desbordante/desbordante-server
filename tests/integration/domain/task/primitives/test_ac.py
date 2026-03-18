import desbordante
import pytest

from src.domain.task.primitives.ac import AcPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.ac.algo_config import BHUNTConfig
from src.schemas.task_schemas.primitives.ac.algo_name import AcAlgoName
from src.schemas.task_schemas.primitives.ac.task_params import (
    AcTaskDatasetsConfig,
    AcTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.domain.task.primitives.constants import PLAYER_STATS_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
)

AC_COLUMNS = ["Strength", "Agility"]


def _ac_range_to_key(
    column_indices: tuple[int, int], ranges: list
) -> tuple[tuple[int, int], tuple]:
    """Convert AC range to comparable key (ranges sorted for order-independent comparison)."""
    sorted_ranges = tuple(tuple(r) for r in sorted(ranges))
    return (column_indices, sorted_ranges)


def _ac_exception_to_key(row_index: int, lhs_value: float, rhs_value: float) -> tuple:
    return (row_index, lhs_value, rhs_value)


@pytest.fixture
def player_stats_ac_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(
        PLAYER_STATS_CSV,
        columns=AC_COLUMNS,
    )


@pytest.fixture
def ac_params(
    player_stats_ac_dataset: TabularDownloadedDatasetSchema,
) -> AcTaskParams[TabularDownloadedDatasetSchema]:
    return AcTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.AC,
        config=BHUNTConfig(
            algo_name=AcAlgoName.BHUNT,
            bin_operation="+",
            p_fuzz=0.85,
            fuzziness=0.2,
            bumps_limit=0,
            weight=0.1,
            ac_seed=11,
            iterations_limit=4,
        ),
        datasets=AcTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=player_stats_ac_dataset
        ),
    )


def test_execute_returns_same_ac_ranges_as_desbordante(
    ac_params: AcTaskParams[TabularDownloadedDatasetSchema],
    player_stats_ac_dataset: TabularDownloadedDatasetSchema,
) -> None:
    table = player_stats_ac_dataset.df

    algo = desbordante.ac.algorithms.Default()
    algo.load_data(table=table)
    algo.execute(
        p_fuzz=0.85,
        fuzziness=0.2,
        bumps_limit=0,
        weight=0.1,
        bin_operation="+",
        ac_seed=11,
        iterations_limit=4,
    )
    desbordante_ranges = algo.get_ac_ranges()
    desbordante_exceptions = algo.get_ac_exceptions()

    primitive = AcPrimitive(algo_name=AcAlgoName.BHUNT)
    primitive_result = primitive.execute(ac_params)

    desbordante_range_keys = {
        _ac_range_to_key(tuple(r.column_indices), r.ranges)  # type: ignore
        for r in desbordante_ranges
    }
    primitive_range_keys = {
        _ac_range_to_key(
            (item.lhs_column.index, item.rhs_column.index),
            item.ranges,
        )
        for item in primitive_result.items
    }
    assert desbordante_range_keys == primitive_range_keys

    exceptions_by_pair: dict[tuple[int, int], set] = {}
    for e in desbordante_exceptions:
        for col_pair in e.column_pairs:
            row = table.iloc[e.row_index]
            key = _ac_exception_to_key(
                e.row_index,
                row[col_pair[0]],
                row[col_pair[1]],
            )
            exceptions_by_pair.setdefault(col_pair, set()).add(key)

    for item in primitive_result.items:
        col_pair = (item.lhs_column.index, item.rhs_column.index)
        primitive_exception_keys = {
            _ac_exception_to_key(ex.row_index, ex.lhs_value, ex.rhs_value)
            for ex in item.exceptions
        }
        desbordante_exception_keys = exceptions_by_pair.get(col_pair, set())
        assert primitive_exception_keys == desbordante_exception_keys
