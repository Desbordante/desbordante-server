from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.ac.types import BinOperation
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class AcExceptionSchema(BaseSchema):
    row_index: int
    lhs_value: float
    rhs_value: float


class AcTaskResultItemField(StrEnum):
    LhsColumn = "lhs_column"
    RhsColumn = "rhs_column"
    Ranges = "ranges"
    Exceptions = "exceptions"


class AcTaskResultItemSchema(BaseSchema):
    lhs_column: ColumnSchema
    rhs_column: ColumnSchema

    ranges: list[tuple[float, float]]
    exceptions: list[AcExceptionSchema]


class AcTaskResultSchema(BaseTaskResultSchema):
    bin_operation: BinOperation


class AcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_column_names: list[str]
    rhs_column_names: list[str]
    lhs_column_indices: list[int]
    rhs_column_indices: list[int]


class AcTaskResultOrderingField(StrEnum):
    LhsColumnName = "lhs_column_name"
    RhsColumnName = "rhs_column_name"
    LhsColumnIndex = "lhs_column_index"
    RhsColumnIndex = "rhs_column_index"
    NumberOfRanges = "number_of_ranges"
    NumberOfExceptions = "number_of_exceptions"
