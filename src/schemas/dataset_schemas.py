import json
from datetime import datetime
from enum import StrEnum, auto
from typing import Annotated, Any, BinaryIO, Literal, Protocol
from uuid import UUID

from pydantic import Field, model_validator

from src.schemas.base_schemas import (
    BaseSchema,
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
    Comma = ","
    Semicolon = ";"
    Pipe = "|"


class DatasetType(StrEnum):
    Tabular = auto()
    Transactional = auto()
    Graph = auto()


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
    type: Literal[DatasetType.Tabular]


class UploadTransactionalDatasetParams(
    TransactionalDatasetParams, BaseUploadDatasetParams
):
    type: Literal[DatasetType.Transactional]


class UploadGraphDatasetParams(GraphDatasetParams, BaseUploadDatasetParams):
    type: Literal[DatasetType.Graph]


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
    pass


class GraphDatasetInfo(BaseSchema):
    number_of_nodes: int
    number_of_edges: int
    is_directed: bool


OneOfDatasetInfo = (
    TabularDatasetInfo | TransactionalDatasetInfo | GraphDatasetInfo | TaskErrorSchema
)


class DatasetSchema(BaseSchema):
    id: UUID
    type: DatasetType
    name: str
    size: int
    params: OneOfDatasetParams

    info: OneOfDatasetInfo | None
    status: TaskStatus

    created_at: datetime
    updated_at: datetime


class DatasetFiltersSchema(BaseSchema):
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
