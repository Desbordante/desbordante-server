from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.ac.types import BinOperation
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AcExceptionSchema(BaseSchema):
    row_index: int
    left_value: float
    right_value: float


class AcTaskResultField(StrEnum):
    LeftIndex = "left_index"
    RightIndex = "right_index"
    LeftColumn = "left_column"
    RightColumn = "right_column"
    Ranges = "ranges"
    Exceptions = "exceptions"


class AcTaskResultItemSchema(BaseSchema):
    left_index: int
    right_index: int
    left_column: str
    right_column: str

    ranges: list[tuple[float, float]]
    exceptions: list[AcExceptionSchema]


class AcTaskResultSchema(BaseTaskResultSchema):
    bin_operation: BinOperation


class AcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left_columns: list[str]
    right_columns: list[str]
    left_indices: list[int]
    right_indices: list[int]


class AcTaskResultOrderingField(StrEnum):
    LeftColumn = "left_column"
    RightColumn = "right_column"
    LeftIndex = "left_index"
    RightIndex = "right_index"
    NumberOfRanges = "number_of_ranges"
    NumberOfExceptions = "number_of_exceptions"
