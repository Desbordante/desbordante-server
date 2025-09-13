import json
from datetime import datetime
from enum import StrEnum, auto
from typing import Annotated, Any, BinaryIO, Literal, Protocol
from uuid import UUID

import networkx as nx
import pandas as pd
from pydantic import ConfigDict, Field, model_validator

from src.schemas.base_schemas import (
    BaseSchema,
    FiltersParamsSchema,
    QueryParamsSchema,
    TaskErrorSchema,
    TaskStatus,
)


class File(Protocol):
    name: str
    data: BinaryIO
    size: int
    content_type: str


class DatasetSeparator(StrEnum):
    COMMA = ","
    SEMICOLON = ";"
    PIPE = "|"


class DatasetType(StrEnum):
    TABULAR = auto()
    TRANSACTIONAL = auto()
    GRAPH = auto()


class SingularTransactionalParams(BaseSchema):
    itemset_format: Literal["singular"]
    id_column: int
    itemset_column: int


class TabularTransactionalParams(BaseSchema):
    itemset_format: Literal["tabular"]
    has_transaction_id: bool


OneOfTransactionalParams = Annotated[
    SingularTransactionalParams | TabularTransactionalParams,
    Field(discriminator="itemset_format"),
]


class NonGraphDatasetParams(BaseSchema):
    has_header: bool
    separator: DatasetSeparator


class TabularDatasetParams(NonGraphDatasetParams):
    pass


class TransactionalDatasetParams(NonGraphDatasetParams):
    transactional_params: OneOfTransactionalParams


class GraphDatasetParams(BaseSchema):
    pass


OneOfDatasetParams = (
    TabularDatasetParams | TransactionalDatasetParams | GraphDatasetParams
)


class BaseUploadDatasetParams(BaseSchema):
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value: Any):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UploadTabularDatasetParams(TabularDatasetParams, BaseUploadDatasetParams):
    type: Literal[DatasetType.TABULAR]


class UploadTransactionalDatasetParams(
    TransactionalDatasetParams, BaseUploadDatasetParams
):
    type: Literal[DatasetType.TRANSACTIONAL]


class UploadGraphDatasetParams(GraphDatasetParams, BaseUploadDatasetParams):
    type: Literal[DatasetType.GRAPH]


OneOfUploadDatasetParams = Annotated[
    UploadTabularDatasetParams
    | UploadTransactionalDatasetParams
    | UploadGraphDatasetParams,
    Field(discriminator="type"),
]


class TabularDatasetInfo(BaseSchema):
    number_of_columns: int
    number_of_rows: int
    column_names: list[str]


class TransactionalDatasetInfo(TabularDatasetInfo):
    unique_values: list[str]


class GraphDatasetInfo(BaseSchema):
    number_of_nodes: int
    number_of_edges: int
    is_directed: bool


OneOfDatasetInfo = TabularDatasetInfo | TransactionalDatasetInfo | GraphDatasetInfo


class DatasetSchema(BaseSchema):
    id: UUID
    type: DatasetType
    name: str
    size: int
    params: OneOfDatasetParams

    info: OneOfDatasetInfo | TaskErrorSchema | None
    status: TaskStatus

    created_at: datetime
    updated_at: datetime


class DatasetFiltersSchema(FiltersParamsSchema):
    type: DatasetType | None = None
    status: TaskStatus | None = None
    min_size: int | None = None
    max_size: int | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None


DatasetQueryParamsSchema = QueryParamsSchema[
    DatasetFiltersSchema, Literal["name", "size", "created_at"]
]


class DatasetsStatsSchema(BaseSchema):
    total_count: int
    total_size: int


class TabularDownloadedDatasetSchema(BaseSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    df: pd.DataFrame
    params: TabularDatasetParams
    info: TabularDatasetInfo


class TransactionalDownloadedDatasetSchema(BaseSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    df: pd.DataFrame
    params: TransactionalDatasetParams
    info: TransactionalDatasetInfo


class GraphDownloadedDatasetSchema(BaseSchema):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    graph: nx.Graph
    params: GraphDatasetParams
    info: GraphDatasetInfo


OneOfDownloadedDatasetSchema = (
    TabularDownloadedDatasetSchema
    | TransactionalDownloadedDatasetSchema
    | GraphDownloadedDatasetSchema
)
