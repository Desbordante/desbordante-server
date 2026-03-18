import pytest
import desbordante

from src.domain.task.primitives.adc import AdcPrimitive
from src.schemas.dataset_schemas import TabularDownloadedDatasetSchema
from src.schemas.task_schemas.primitives.adc.algo_config import FastAdcConfig
from src.schemas.task_schemas.primitives.adc.algo_name import AdcAlgoName
from src.schemas.task_schemas.primitives.adc.task_params import (
    AdcTaskDatasetsConfig,
    AdcTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName

from tests.integration.domain.task.primitives.constants import TAXES_1_CSV
from tests.integration.domain.task.primitives.helpers import (
    load_tabular_dataset_from_csv,
)

ADC_EVIDENCE_THRESHOLD = 0
ADC_SHARD_LENGTH = 0


@pytest.fixture
def taxes_1_dataset() -> TabularDownloadedDatasetSchema:
    return load_tabular_dataset_from_csv(TAXES_1_CSV)


@pytest.fixture
def adc_params(
    taxes_1_dataset: TabularDownloadedDatasetSchema,
) -> AdcTaskParams[TabularDownloadedDatasetSchema]:
    return AdcTaskParams[TabularDownloadedDatasetSchema](
        primitive_name=PrimitiveName.ADC,
        config=FastAdcConfig(
            algo_name=AdcAlgoName.FAST_ADC,
            evidence_threshold=ADC_EVIDENCE_THRESHOLD,
            shard_length=ADC_SHARD_LENGTH,
        ),
        datasets=AdcTaskDatasetsConfig[TabularDownloadedDatasetSchema](
            table=taxes_1_dataset
        ),
    )


def test_execute_returns_same_dcs_as_desbordante(
    adc_params: AdcTaskParams[TabularDownloadedDatasetSchema],
) -> None:
    algo = desbordante.dc.algorithms.FastADC()
    algo.load_data(table=(TAXES_1_CSV, ",", True))
    algo.execute(
        evidence_threshold=ADC_EVIDENCE_THRESHOLD,
        shard_length=ADC_SHARD_LENGTH,
    )
    desbordante_dcs = algo.get_dcs()

    primitive = AdcPrimitive(algo_name=AdcAlgoName.FAST_ADC)
    primitive_result = primitive.execute(adc_params)

    assert len(primitive_result.items) == len(desbordante_dcs)
    assert primitive_result.result.total_count == len(desbordante_dcs)
