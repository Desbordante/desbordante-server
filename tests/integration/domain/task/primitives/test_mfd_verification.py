import desbordante
import pytest

from src.domain.task.primitives.mfd_verification import MfdVerificationPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.mfd_verification.algo_config import (
    MetricVerifierConfig,
)
from src.schemas.task_schemas.primitives.mfd_verification.algo_name import (
    MfdVerificationAlgoName,
)
from src.schemas.task_schemas.primitives.mfd_verification.task_params import (
    MfdVerificationTaskDatasetsConfig,
    MfdVerificationTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName
from tests.integration.domain.task.primitives.constants import THEATRES_MFD_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
)

MFD_VERIFICATION_LHS_INDICES = [0]
MFD_VERIFICATION_RHS_INDICES = [2]
MFD_VERIFICATION_PARAMETER = 3.0


@pytest.fixture
def theatres_mfd_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(THEATRES_MFD_CSV)


@pytest.fixture
def mfd_verification_params(
    theatres_mfd_dataset: TabularDownloadedDatasetSchema,
) -> MfdVerificationTaskParams[TabularDownloadedDatasetSchema]:
    return MfdVerificationTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.MFD_VERIFICATION,
        config=MetricVerifierConfig(
            algo_name=MfdVerificationAlgoName.METRIC_VERIFIER,
            lhs_indices=MFD_VERIFICATION_LHS_INDICES,
            rhs_indices=MFD_VERIFICATION_RHS_INDICES,
            parameter=MFD_VERIFICATION_PARAMETER,
        ),
        datasets=MfdVerificationTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=theatres_mfd_dataset
        ),
    )


def test_execute_returns_same_result_as_desbordante(
    mfd_verification_params: MfdVerificationTaskParams[TabularDownloadedDatasetSchema],
    theatres_mfd_dataset: TabularDownloadedDatasetSchema,
) -> None:
    table = theatres_mfd_dataset.df

    algo = desbordante.mfd_verification.algorithms.MetricVerifier()
    algo.load_data(table=table)
    algo.execute(
        lhs_indices=MFD_VERIFICATION_LHS_INDICES,
        rhs_indices=MFD_VERIFICATION_RHS_INDICES,
        parameter=MFD_VERIFICATION_PARAMETER,
        metric="euclidean",
    )
    desbordante_mfd_holds = algo.mfd_holds()
    desbordante_clusters = algo.get_highlights()

    primitive = MfdVerificationPrimitive(
        algo_name=MfdVerificationAlgoName.METRIC_VERIFIER
    )
    primitive_result = primitive.execute(mfd_verification_params)

    assert primitive_result.result.mfd_holds == desbordante_mfd_holds

    if not desbordante_mfd_holds:
        desbordante_keys = {
            (
                tuple(sorted(h.data_index for h in cluster)),
                round(max(h.max_distance for h in cluster), 10),
            )
            for cluster in desbordante_clusters
        }
        primitive_keys = {
            (
                tuple(sorted(h.data_index for h in item.highlights)),
                round(item.max_distance, 10),
            )
            for item in primitive_result.items
        }
        assert desbordante_keys == primitive_keys
