from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AfdTaskResultItemSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_columns: list[str]
    rhs_index: int
    rhs_column: str


class AfdTaskResultItemField(StrEnum):
    LhsIndices = "lhs_indices"
    LhsColumns = "lhs_columns"
    RhsIndex = "rhs_index"
    RhsColumn = "rhs_column"


class AfdTaskResultSchema(BaseTaskResultSchema):
    pass


class AfdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_indices: list[int]
    lhs_columns: list[str]
    rhs_index: int
    rhs_column: str


class AfdTaskResultOrderingField(StrEnum):
    LhsIndices = "lhs_indices"
    LhsColumns = "lhs_columns"
    RhsIndex = "rhs_index"
    RhsColumn = "rhs_column"
    NumberOfLhsColumns = "number_of_lhs_columns"
