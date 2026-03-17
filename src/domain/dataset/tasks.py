import asyncio

from src.domain.dataset.dependencies import get_storage
from src.domain.dataset.utils import (
    get_graph_info,
    get_tabular_info,
    get_transactional_info,
)
from src.schemas.dataset_schemas import (
    DatasetType,
    GraphDatasetParams,
    OneOfDatasetInfo,
    OneOfDatasetParams,
    TabularDatasetParams,
    TransactionalDatasetParams,
)
from src.worker.config import settings
from src.worker.dataset_task_backend import PreprocessingTaskBackend
from src.worker.worker import worker


@worker.task(
    name="tasks.preprocess_dataset",
    backend=PreprocessingTaskBackend(app=worker, url=settings.database_url),
    pydantic=True,
    bind=True,
)
def preprocess_dataset(
    self, *, type: DatasetType, params: OneOfDatasetParams, path: str
) -> OneOfDatasetInfo:

    async def _run():
        storage = await get_storage()
        return await storage.download(path=path)

    data = asyncio.run(_run())

    match type:
        case DatasetType.TABULAR:
            params = TabularDatasetParams.model_validate(params)
            return get_tabular_info(params, data)
        case DatasetType.TRANSACTIONAL:
            params = TransactionalDatasetParams.model_validate(params)
            return get_transactional_info(params, data)
        case DatasetType.GRAPH:
            params = GraphDatasetParams.model_validate(params)
            return get_graph_info(params, data)
