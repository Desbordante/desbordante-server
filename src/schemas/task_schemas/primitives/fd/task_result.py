from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class FdTaskResultItemSchema(BaseSchema):
    lhs_columns: list[ColumnSchema]
    rhs_column: ColumnSchema


class FdTaskResultItemField(StrEnum):
    LHS_COLUMNS = "lhs_columns"
    RHS_COLUMN = "rhs_column"


class FdTaskResultSchema(BaseTaskResultSchema):
    pass


class FdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_columns_indices: list[int]
    lhs_columns_names: list[str]
    rhs_column_indices: list[int]
    rhs_column_names: list[str]


class FdTaskResultOrderingField(StrEnum):
    LHS_COLUMNS_INDICES = "lhs_columns_indices"
    LHS_COLUMNS_NAMES = "lhs_columns_names"
    RHS_COLUMN_INDEX = "rhs_column_index"
    RHS_COLUMN_NAME = "rhs_column_name"
    NUMBER_OF_LHS_COLUMNS = "number_of_lhs_columns"
