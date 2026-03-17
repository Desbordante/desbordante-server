from uuid import UUID

from src.domain.dataset.tasks import preprocess_dataset


class PreprocessDatasetWorker:
    def run(self, *, task_id: UUID, dataset_id: UUID) -> None:
        preprocess_dataset.apply_async(args=(dataset_id,), task_id=str(task_id))
