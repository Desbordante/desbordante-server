from enum import StrEnum


from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AfdTaskResultItemSchema(BaseSchema):
    left_indices: list[int]
    left_columns: list[str]
    right_index: int
    right_column: str


class AfdTaskResultItemField(StrEnum):
    LeftIndices = "left_indices"
    LeftColumns = "left_columns"
    RightIndex = "right_index"
    RightColumn = "right_column"


class AfdTaskResultSchema(BaseTaskResultSchema):
    pass


class AfdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left_indices: list[int]
    left_columns: list[str]
    right_index: int
    right_column: str


class AfdTaskResultOrderingField(StrEnum):
    LeftIndices = "left_indices"
    LeftColumns = "left_columns"
    RightIndex = "right_index"
    RightColumn = "right_column"
    NumberOfLeftColumns = "number_of_left_columns"
