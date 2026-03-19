import desbordante
import pytest

from src.domain.task.primitives.fd_verification import FdVerificationPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.fd_verification.algo_config import (
    FdVerifierConfig,
)
from src.schemas.task_schemas.primitives.fd_verification.algo_name import (
    FdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.fd_verification.task_params import (
    FdVerificationTaskDatasetsConfig,
    FdVerificationTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.domain.task.primitives.constants import DUPLICATES_SHORT_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
)

FD_VERIFICATION_LHS_INDICES = [1]
FD_VERIFICATION_RHS_INDICES = [2]


def _highlight_to_key(highlight) -> tuple:
    """Convert highlight to comparable key."""
    cluster = tuple(sorted(highlight.cluster))
    return (
        highlight.num_distinct_rhs_values,
        highlight.most_frequent_rhs_value_proportion,
        cluster,
    )


@pytest.fixture
def duplicates_short_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(DUPLICATES_SHORT_CSV)


@pytest.fixture
def fd_verification_params(
    duplicates_short_dataset: TabularDownloadedDatasetSchema,
) -> FdVerificationTaskParams[TabularDownloadedDatasetSchema]:
    return FdVerificationTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.FD_VERIFICATION,
        config=FdVerifierConfig(
            algo_name=FdVerificationAlgoName.FD_VERIFIER,
            lhs_indices=FD_VERIFICATION_LHS_INDICES,
            rhs_indices=FD_VERIFICATION_RHS_INDICES,
            is_null_equal_null=False,
        ),
        datasets=FdVerificationTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=duplicates_short_dataset
        ),
    )


def test_execute_returns_same_result_as_desbordante(
    fd_verification_params: FdVerificationTaskParams[TabularDownloadedDatasetSchema],
    duplicates_short_dataset: TabularDownloadedDatasetSchema,
) -> None:
    table = duplicates_short_dataset.df

    algo = desbordante.fd_verification.algorithms.FDVerifier()
    algo.load_data(table=table)
    algo.execute(
        lhs_indices=FD_VERIFICATION_LHS_INDICES,
        rhs_indices=FD_VERIFICATION_RHS_INDICES,
        is_null_equal_null=False,
    )
    desbordante_fd_holds = algo.fd_holds()
    desbordante_highlights = algo.get_highlights()
    desbordante_error = algo.get_error()
    desbordante_num_clusters = algo.get_num_error_clusters()
    desbordante_num_rows = algo.get_num_error_rows()

    primitive = FdVerificationPrimitive(algo_name=FdVerificationAlgoName.FD_VERIFIER)
    primitive_result = primitive.execute(fd_verification_params)

    assert primitive_result.result.fd_holds == desbordante_fd_holds
    assert primitive_result.result.error == desbordante_error
    assert primitive_result.result.number_of_error_clusters == desbordante_num_clusters
    assert primitive_result.result.number_of_error_rows == desbordante_num_rows

    if not desbordante_fd_holds:
        desbordante_keys = {_highlight_to_key(h) for h in desbordante_highlights}
        primitive_keys = {
            (
                item.number_of_distinct_rhs_values,
                item.most_frequent_rhs_value_proportion,
                tuple(sorted(r.row_index for r in item.rows)),
            )
            for item in primitive_result.items
        }
        assert desbordante_keys == primitive_keys
