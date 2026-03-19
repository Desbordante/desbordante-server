import pytest
import desbordante

from src.domain.task.primitives.ar import ArPrimitive
from src.schemas.dataset_schemas import TransactionalDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.ar.algo_config import AprioriConfig
from src.schemas.task_schemas.primitives.ar.algo_name import ArAlgoName
from src.schemas.task_schemas.primitives.ar.task_params import (
    ArTaskDatasetsConfig,
    ArTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import RULES_BOOK_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_transactional_dataset_from_csv,
)

AR_MINSUP = 0.4
AR_MINCONF = 0.6


def _ar_to_key(
    lhs_values: list, rhs_values: list, support: float, confidence: float
) -> tuple:
    """Convert AR to comparable key (lhs/rhs order preserved for AR semantics)."""
    return (
        tuple(lhs_values),
        tuple(rhs_values),
        round(support, 10),
        round(confidence, 10),
    )


@pytest.fixture
def rules_book_dataset() -> TransactionalDownloadedDatasetSchema:
    return load_transactional_dataset_from_csv(
        RULES_BOOK_CSV,
        has_header=False,
        itemset_format="singular",
        id_column=0,
        itemset_column=1,
    )


@pytest.fixture
def ar_params(
    rules_book_dataset: TransactionalDownloadedDatasetSchema,
) -> ArTaskParams[TransactionalDownloadedDatasetSchema]:
    return ArTaskParams[TransactionalDownloadedDatasetSchema](
        primitive_name=PrimitiveName.AR,
        config=AprioriConfig(
            algo_name=ArAlgoName.APRIORI,
            minsup=AR_MINSUP,
            minconf=AR_MINCONF,
        ),
        datasets=ArTaskDatasetsConfig[TransactionalDownloadedDatasetSchema](
            table=rules_book_dataset
        ),
    )


def test_execute_returns_same_ars_as_desbordante(
    ar_params: ArTaskParams[TransactionalDownloadedDatasetSchema],
) -> None:
    algo = desbordante.ar.algorithms.Default()
    algo.load_data(
        table=(RULES_BOOK_CSV, ",", False),
        input_format="singular",
    )
    algo.execute(minsup=AR_MINSUP, minconf=AR_MINCONF)
    desbordante_ars = algo.get_ars()

    primitive = ArPrimitive(algo_name=ArAlgoName.APRIORI)
    primitive_result = primitive.execute(ar_params)

    desbordante_keys = {
        _ar_to_key(
            list(ar.left),
            list(ar.right),
            ar.support,
            ar.confidence,
        )
        for ar in desbordante_ars
    }
    primitive_keys = {
        _ar_to_key(
            item.lhs_values,
            item.rhs_values,
            item.support,
            item.confidence,
        )
        for item in primitive_result.items
    }

    assert desbordante_keys == primitive_keys
