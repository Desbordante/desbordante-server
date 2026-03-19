import asyncio
from io import BytesIO

import networkx as nx
import pandas as pd
from networkx.drawing import nx_pydot

from src.infrastructure.storage.client import get_storage
from src.schemas.dataset_schemas import (
    DatasetForTaskSchema,
    DatasetType,
    GraphDatasetInfo,
    GraphDatasetParams,
    GraphDownloadedDatasetSchema,
    OneOfDownloadedDatasetSchema,
    TabularDatasetInfo,
    TabularDatasetParams,
    TabularDownloadedDatasetSchema,
    TransactionalDatasetInfo,
    TransactionalDatasetParams,
    TransactionalDownloadedDatasetSchema,
)


def download_dataset(dataset: DatasetForTaskSchema) -> OneOfDownloadedDatasetSchema:
    async def _run():
        storage = get_storage()
        return await storage.download(path=dataset.path)

    data = asyncio.run(_run())

    match dataset.type:
        case DatasetType.TABULAR:
            params = TabularDatasetParams.model_validate(dataset.params)
            info = TabularDatasetInfo.model_validate(dataset.preprocessing.result)
            df = pd.read_csv(  # type: ignore
                BytesIO(data),
                sep=params.separator,
                header=0 if params.has_header else None,
            )
            return TabularDownloadedDatasetSchema(df=df, params=params, info=info)
        case DatasetType.TRANSACTIONAL:
            params = TransactionalDatasetParams.model_validate(dataset.params)
            info = TransactionalDatasetInfo.model_validate(dataset.preprocessing.result)
            df = pd.read_csv(  # type: ignore
                BytesIO(data),
                sep=params.separator,
                header=0 if params.has_header else None,
            )
            return TransactionalDownloadedDatasetSchema(df=df, params=params, info=info)

        case DatasetType.GRAPH:
            graph = nx.Graph(nx_pydot.read_dot(BytesIO(data)))  # type: ignore
            params = GraphDatasetParams.model_validate(dataset.params)
            info = GraphDatasetInfo.model_validate(dataset.preprocessing.result)
            return GraphDownloadedDatasetSchema(graph=graph, params=params, info=info)
