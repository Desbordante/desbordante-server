from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class AfdTaskResultItemSchema(BaseSchema):
    lhs_columns: list[ColumnSchema]
    rhs_column: ColumnSchema


class AfdTaskResultItemField(StrEnum):
    LhsColumns = "lhs_columns"
    RhsColumn = "rhs_column"


class AfdTaskResultSchema(BaseTaskResultSchema):
    pass


class AfdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_columns_indices: list[int]
    lhs_columns_names: list[str]
    rhs_column_indices: list[int]
    rhs_column_names: list[str]


class AfdTaskResultOrderingField(StrEnum):
    LhsColumnsIndices = "lhs_columns_indices"
    LhsColumnsNames = "lhs_columns_names"
    RhsColumnIndex = "rhs_column_index"
    RhsColumnName = "rhs_column_name"
    NumberOfLhsColumns = "number_of_lhs_columns"
