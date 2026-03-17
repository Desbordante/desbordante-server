from uuid import UUID

from src.domain.dataset.tasks import preprocess_dataset
from src.schemas.dataset_schemas import DatasetType, OneOfDatasetParams


class PreprocessDatasetWorker:
    def run(
        self, *, type: DatasetType, params: OneOfDatasetParams, path: str, task_id: UUID
    ) -> None:
        preprocess_dataset.apply_async(
            kwargs={
                "type": type,
                "params": params,
                "path": path,
            },
            task_id=str(task_id),
        )
