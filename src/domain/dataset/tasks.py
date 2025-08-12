from uuid import UUID

from src.crud.dataset_crud import DatasetCrud
from src.domain.dataset.storage import storage
from src.domain.dataset.utils import (
    get_graph_info,
    get_tabular_info,
    get_transactional_info,
)
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import (
    DatasetType,
    GraphDatasetParams,
    OneOfDatasetInfo,
    TabularDatasetParams,
    TransactionalDatasetParams,
)
from src.worker.task import DatabaseTaskBase
from src.worker.worker import worker


class PreprocessDatasetTask(DatabaseTaskBase[DatasetModel, UUID]):
    crud_class = DatasetCrud
    result_field = "info"


@worker.task(name="tasks.preprocess_dataset", base=PreprocessDatasetTask, bind=True)
def preprocess_dataset(
    self: PreprocessDatasetTask, dataset_id: UUID
) -> OneOfDatasetInfo:
    dataset = self.entity
    data = storage.download_file_sync(path=dataset.path)

    match dataset.type:
        case DatasetType.Tabular:
            params = TabularDatasetParams.model_validate(dataset.params)
            return get_tabular_info(params, data)
        case DatasetType.Transactional:
            params = TransactionalDatasetParams.model_validate(dataset.params)
            return get_transactional_info(params, data)
        case DatasetType.Graph:
            params = GraphDatasetParams.model_validate(dataset.params)
            return get_graph_info(params, data)
