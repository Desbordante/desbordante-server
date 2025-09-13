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
    LHS_COLUMN = "lhs_column"
    RHS_COLUMN = "rhs_column"
    RANGES = "ranges"
    EXCEPTIONS = "exceptions"


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
    LHS_COLUMN_NAME = "lhs_column_name"
    RHS_COLUMN_NAME = "rhs_column_name"
    LHS_COLUMN_INDEX = "lhs_column_index"
    RHS_COLUMN_INDEX = "rhs_column_index"
    NUMBER_OF_RANGES = "number_of_ranges"
    NUMBER_OF_EXCEPTIONS = "number_of_exceptions"
