# type: ignore
from io import BytesIO

import networkx as nx
import pandas as pd
from networkx.drawing import nx_pydot

from src.schemas.dataset_schemas import (
    GraphDatasetInfo,
    GraphDatasetParams,
    TabularDatasetInfo,
    TabularDatasetParams,
    TransactionalDatasetInfo,
    TransactionalDatasetParams,
)


def get_graph_info(params: GraphDatasetParams, data: bytes) -> GraphDatasetInfo:
    """
    Extract graph information from graph data using NetworkX.
    """
    G = nx.Graph(nx_pydot.read_dot(BytesIO(data)))

    return GraphDatasetInfo(
        number_of_nodes=G.number_of_nodes(),
        number_of_edges=G.number_of_edges(),
        is_directed=G.is_directed(),
    )


def get_tabular_info(params: TabularDatasetParams, data: bytes) -> TabularDatasetInfo:
    """
    Extract tabular dataset information using Pandas.
    """
    df = pd.read_csv(
        BytesIO(data),
        sep=params.separator,
        header=0 if params.has_header else None,
    )

    return TabularDatasetInfo(
        number_of_columns=df.shape[1],
        number_of_rows=df.shape[0],
        column_names=list(map(str, df.columns)),
    )


def get_transactional_info(
    params: TransactionalDatasetParams, data: bytes
) -> TransactionalDatasetInfo:
    """
    Extract transactional dataset information using Pandas.
    """
    result = get_tabular_info(params, data)

    return TransactionalDatasetInfo(**result)
