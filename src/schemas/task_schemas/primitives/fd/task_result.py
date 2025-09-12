from enum import StrEnum


from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class FdTaskResultItemSchema(BaseSchema):
    left_indices: list[int]
    left_columns: list[str]
    right_index: int
    right_column: str


class FdTaskResultItemField(StrEnum):
    LeftIndices = "left_indices"
    LeftColumns = "left_columns"
    RightIndex = "right_index"
    RightColumn = "right_column"


class FdTaskResultSchema(BaseTaskResultSchema):
    pass


class FdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left_indices: list[int]
    left_columns: list[str]
    right_index: int
    right_column: str


class FdTaskResultOrderingField(StrEnum):
    LeftIndices = "left_indices"
    LeftColumns = "left_columns"
    RightIndex = "right_index"
    RightColumn = "right_column"
    NumberOfLeftColumns = "number_of_left_columns"
