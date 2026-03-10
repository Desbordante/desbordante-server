import asyncio
from typing import Any, Coroutine, TypeVar
from uuid import UUID

from src.crud.dataset_crud import DatasetCrud
from src.domain.dataset.dependencies import get_storage
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

T = TypeVar("T")


def _run_async(coro: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coro)


class PreprocessDatasetTask(DatabaseTaskBase[DatasetModel, UUID]):
    crud_class = DatasetCrud
    result_field = "info"


@worker.task(name="tasks.preprocess_dataset", base=PreprocessDatasetTask, bind=True)
def preprocess_dataset(
    self: PreprocessDatasetTask, dataset_id: UUID
) -> OneOfDatasetInfo:
    dataset = self.entity

    async def _run():
        storage = await get_storage()
        return await storage.download(path=dataset.path)

    data = _run_async(_run())

    match dataset.type:
        case DatasetType.TABULAR:
            params = TabularDatasetParams.model_validate(dataset.params)
            return get_tabular_info(params, data)
        case DatasetType.TRANSACTIONAL:
            params = TransactionalDatasetParams.model_validate(dataset.params)
            return get_transactional_info(params, data)
        case DatasetType.GRAPH:
            params = GraphDatasetParams.model_validate(dataset.params)
            return get_graph_info(params, data)
