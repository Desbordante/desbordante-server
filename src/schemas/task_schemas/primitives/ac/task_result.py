from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.ac.types import BinOperation
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AcExceptionSchema(BaseSchema):
    row_index: int
    lhs_value: float
    rhs_value: float


class AcTaskResultItemField(StrEnum):
    LhsIndex = "lhs_index"
    RhsIndex = "rhs_index"
    LhsColumn = "lhs_column"
    RhsColumn = "rhs_column"
    Ranges = "ranges"
    Exceptions = "exceptions"


class AcTaskResultItemSchema(BaseSchema):
    lhs_index: int
    rhs_index: int
    lhs_column: str
    rhs_column: str

    ranges: list[tuple[float, float]]
    exceptions: list[AcExceptionSchema]


class AcTaskResultSchema(BaseTaskResultSchema):
    bin_operation: BinOperation


class AcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_columns: list[str]
    rhs_columns: list[str]
    lhs_indices: list[int]
    rhs_indices: list[int]


class AcTaskResultOrderingField(StrEnum):
    LhsColumn = "lhs_column"
    RhsColumn = "rhs_column"
    LhsIndex = "lhs_index"
    RhsIndex = "rhs_index"
    NumberOfRanges = "number_of_ranges"
    NumberOfExceptions = "number_of_exceptions"
