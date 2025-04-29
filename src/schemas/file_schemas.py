from datetime import datetime
from enum import StrEnum, auto
from typing import Annotated, BinaryIO, Literal, Protocol, Union
from uuid import UUID

from pydantic import Field

from src.schemas.base_schemas import BaseSchema


class FileType(StrEnum):
    Dataset = auto()
    Media = auto()


class File(Protocol):
    type: FileType
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
    number_of_columns: int
    number_of_rows: int
    column_names: list[str]


class TabularDatasetParams(NonGraphDatasetParams):
    type: Literal[DatasetType.Tabular]


class TransactionalDatasetParams(NonGraphDatasetParams):
    type: Literal[DatasetType.Transactional]
    transactional_params: OneOfTransactionalParams


class GraphDatasetParams(BaseSchema):
    type: Literal[DatasetType.Graph]


OneOfDatasetParams = Annotated[
    TabularDatasetParams | TransactionalDatasetParams | GraphDatasetParams,
    Field(discriminator="type"),
]


class UploadTabularDatasetSchema(BaseSchema):
    type: Literal[DatasetType.Tabular] = DatasetType.Tabular
    has_header: bool
    separator: DatasetSeparator


class UploadTransactionalDatasetSchema(BaseSchema):
    type: Literal[DatasetType.Transactional]
    has_header: bool
    separator: DatasetSeparator
    transactional_params: OneOfTransactionalParams


class UploadGraphDatasetSchema(BaseSchema):
    type: Literal[DatasetType.Graph]


OneOfUploadDatasetSchema = Annotated[
    Union[
        UploadTabularDatasetSchema,
        UploadTransactionalDatasetSchema,
        UploadGraphDatasetSchema,
    ],
    Field(discriminator="type"),
]


class FileSchema(BaseSchema):
    id: UUID
    name: str
    byte_size: int

    owner_id: int


class DatasetSchema(BaseSchema):
    id: UUID
    type: DatasetType

    params: OneOfDatasetParams

    file: FileSchema

    created_at: datetime


class DatasetSortField(StrEnum):
    """Fields that can be used for sorting datasets"""

    NAME = "name"
    SIZE = "size"
    CREATED_AT = "created_at"


class SortDirection(StrEnum):
    """Sort direction options"""

    ASC = "asc"
    DESC = "desc"


class DatasetOrderingSchema(BaseSchema):
    """Schema for ordering datasets"""

    field: DatasetSortField
    direction: SortDirection = SortDirection.ASC


class DatasetFilterSchema(BaseSchema):
    """Schema for filtering datasets"""

    min_size: int | None = None
    max_size: int | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    search: str | None = None


class DatasetQueryParamsSchema(BaseSchema):
    """Combined schema for all dataset query parameters"""

    filters: DatasetFilterSchema = Field(default_factory=DatasetFilterSchema)
    ordering: DatasetOrderingSchema | None = None
    limit: int = 100
    offset: int = 0
