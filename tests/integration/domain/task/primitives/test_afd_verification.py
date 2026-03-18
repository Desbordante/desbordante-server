import pytest
import desbordante

from src.domain.task.primitives.afd_verification import AfdVerificationPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.afd_verification.algo_config import (
    AfdVerifierConfig,
)
from src.schemas.task_schemas.primitives.afd_verification.algo_name import (
    AfdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.afd_verification.task_params import (
    AfdVerificationTaskDatasetsConfig,
    AfdVerificationTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import DUPLICATES_SHORT_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
)

AFD_VERIFICATION_LHS_INDICES = [1]
AFD_VERIFICATION_RHS_INDICES = [2]


def _highlight_to_key(highlight, table) -> tuple:
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
def afd_verification_params(
    duplicates_short_dataset: TabularDownloadedDatasetSchema,
) -> AfdVerificationTaskParams[TabularDownloadedDatasetSchema]:
    return AfdVerificationTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.AFD_VERIFICATION,
        config=AfdVerifierConfig(
            algo_name=AfdVerificationAlgoName.AFD_VERIFIER,
            lhs_indices=AFD_VERIFICATION_LHS_INDICES,
            rhs_indices=AFD_VERIFICATION_RHS_INDICES,
        ),
        datasets=AfdVerificationTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=duplicates_short_dataset
        ),
    )


def test_execute_returns_same_result_as_desbordante(
    afd_verification_params: AfdVerificationTaskParams[TabularDownloadedDatasetSchema],
    duplicates_short_dataset: TabularDownloadedDatasetSchema,
) -> None:
    table = duplicates_short_dataset.df

    algo = desbordante.fd_verification.algorithms.FDVerifier()
    algo.load_data(table=table)
    algo.execute(
        lhs_indices=AFD_VERIFICATION_LHS_INDICES,
        rhs_indices=AFD_VERIFICATION_RHS_INDICES,
    )
    desbordante_fd_holds = algo.fd_holds()
    desbordante_highlights = algo.get_highlights()
    desbordante_error = algo.get_error()
    desbordante_num_clusters = algo.get_num_error_clusters()
    desbordante_num_rows = algo.get_num_error_rows()

    primitive = AfdVerificationPrimitive(algo_name=AfdVerificationAlgoName.AFD_VERIFIER)
    primitive_result = primitive.execute(afd_verification_params)

    assert primitive_result.result.fd_holds == desbordante_fd_holds
    assert primitive_result.result.error == desbordante_error
    assert primitive_result.result.number_of_error_clusters == desbordante_num_clusters
    assert primitive_result.result.number_of_error_rows == desbordante_num_rows

    if not desbordante_fd_holds:
        desbordante_keys = {_highlight_to_key(h, table) for h in desbordante_highlights}
        primitive_keys = {
            (
                item.number_of_distinct_rhs_values,
                item.most_frequent_rhs_value_proportion,
                tuple(sorted(r.row_index for r in item.rows)),
            )
            for item in primitive_result.items
        }
        assert desbordante_keys == primitive_keys
