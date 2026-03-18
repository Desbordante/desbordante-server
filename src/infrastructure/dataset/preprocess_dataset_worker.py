from uuid import UUID

from src.domain.dataset.tasks import preprocess_dataset
from src.schemas.dataset_schemas import DatasetForTaskSchema


class PreprocessDatasetWorker:
    def run(self, *, dataset: DatasetForTaskSchema, task_id: UUID) -> None:
        preprocess_dataset.apply_async(
            kwargs={
                "dataset": dataset,
            },
            task_id=str(task_id),
        )
