from typing import Any
from uuid import UUID

from src.crud.dataset_crud import DatasetCrud
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import NonGraphDatasetInfo
from src.worker.task import DatabaseTaskBase
from src.worker.worker import worker


class PreprocessDatasetTask(DatabaseTaskBase[DatasetModel, UUID]):
    crud_class = DatasetCrud
    result_field = "info"


@worker.task(name="tasks.preprocess_dataset", base=PreprocessDatasetTask, bind=True)
def preprocess_dataset(self: PreprocessDatasetTask, dataset_id: UUID) -> Any:
    import time

    time.sleep(5)  # Имитация 5-секундной задержки обработки

    print("TETSTSTTSTSTS", self.entity)
    return NonGraphDatasetInfo(
        number_of_columns=10,
        number_of_rows=100,
        column_names=["col1", "col2", "col3"],
    )
