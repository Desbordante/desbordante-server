"""Backend for preprocessing (dataset) task result storage."""

from src.infrastructure.bg_tasks.base_task_backend import BaseTaskBackend
from src.models.dataset_models import PreprocessingTaskModel


class PreprocessDatasetBackend(BaseTaskBackend[PreprocessingTaskModel]):
    task_cls = PreprocessingTaskModel
