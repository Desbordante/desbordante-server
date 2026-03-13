from uuid import UUID

from src.domain.dataset.tasks import preprocess_dataset


class PreprocessDatasetWorker:
    def set(self, *, dataset_id: UUID) -> str:
        result = preprocess_dataset.delay(dataset_id)
        return result.id
