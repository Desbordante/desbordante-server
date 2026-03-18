import asyncio

from src.domain.dataset.dependencies import get_storage
from src.domain.dataset.utils import (
    get_graph_info,
    get_tabular_info,
    get_transactional_info,
)
from src.infrastructure.bg_tasks.preprocess_dataset.backend import (
    PreprocessDatasetBackend,
)
from src.infrastructure.bg_tasks.resource_intensive_task import ResourceIntensiveTask
from src.schemas.dataset_schemas import (
    DatasetForTaskSchema,
    DatasetType,
    GraphDatasetParams,
    OneOfDatasetInfo,
    TabularDatasetParams,
    TransactionalDatasetParams,
)
from src.infrastructure.bg_tasks.config import settings
from src.worker.worker import worker


@worker.task(
    name="tasks.preprocess_dataset",
    backend=PreprocessDatasetBackend(app=worker, url=settings.database_url),
    base=ResourceIntensiveTask,
    pydantic=True,
    bind=True,
)
def preprocess_dataset(self, *, dataset: DatasetForTaskSchema) -> OneOfDatasetInfo:

    async def _run():
        storage = await get_storage()
        return await storage.download(path=dataset.path)

    data = asyncio.run(_run())

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
