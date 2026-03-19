"""Helper functions for task CRUD tests."""

from src.models.dataset_models import DatasetModel
from src.models.task_models import ProfilingTaskModel
from src.schemas.task_schemas.primitives.fd.algo_config import HyFDConfig
from src.schemas.task_schemas.primitives.fd.algo_name import FdAlgoName
from src.schemas.task_schemas.primitives.fd.task_params import (
    FdTaskDatasetsConfig,
    FdTaskParams,
)
from src.schemas.task_schemas.types import PrimitiveName


def make_task_entity(
    *,
    datasets: list[DatasetModel],
    owner_id: int | None = None,
    is_public: bool = False,
) -> ProfilingTaskModel:
    params = FdTaskParams(
        primitive_name=PrimitiveName.FD,
        config=HyFDConfig(algo_name=FdAlgoName.HY_FD),
        datasets=FdTaskDatasetsConfig(table=datasets[0].id),
    )
    return ProfilingTaskModel(
        params=params,
        datasets=datasets,
        owner_id=owner_id,
        is_public=is_public,
    )
