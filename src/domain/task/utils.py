from io import BytesIO

import networkx as nx
import pandas as pd
from networkx.drawing import nx_pydot

from src.domain.dataset.storage import storage
from src.models.dataset_models import DatasetModel
from src.schemas.dataset_schemas import (
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


def download_dataset(dataset: DatasetModel) -> OneOfDownloadedDatasetSchema:
    data = storage.download_file_sync(path=dataset.path)

    match dataset.type:
        case DatasetType.Tabular:
            params = TabularDatasetParams.model_validate(dataset.params)
            info = TabularDatasetInfo.model_validate(dataset.info)
            df = pd.read_csv(  # type: ignore
                BytesIO(data),
                sep=params.separator,
                header=0 if params.has_header else None,
            )
            return TabularDownloadedDatasetSchema(df=df, params=params, info=info)
        case DatasetType.Transactional:
            params = TransactionalDatasetParams.model_validate(dataset.params)
            info = TransactionalDatasetInfo.model_validate(dataset.info)
            df = pd.read_csv(  # type: ignore
                BytesIO(data),
                sep=params.separator,
                header=0 if params.has_header else None,
            )
            return TransactionalDownloadedDatasetSchema(df=df, params=params, info=info)

        case DatasetType.Graph:
            graph = nx.Graph(nx_pydot.read_dot(BytesIO(data)))  # type: ignore
            params = GraphDatasetParams.model_validate(dataset.params)
            info = GraphDatasetInfo.model_validate(dataset.info)
            return GraphDownloadedDatasetSchema(graph=graph, params=params, info=info)
