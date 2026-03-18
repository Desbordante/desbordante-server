"""Backend for preprocessing (dataset) task result storage."""

from src.models.dataset_models import PreprocessingTaskModel
from src.worker.base_task_backend import BaseTaskBackend


class PreprocessingTaskBackend(BaseTaskBackend[PreprocessingTaskModel]):
    task_cls = PreprocessingTaskModel
