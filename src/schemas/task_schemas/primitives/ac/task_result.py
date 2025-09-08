from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AcTaskResultItemSchema(BaseSchema):
    left_column_index: int
    right_column_index: int
    left_column_name: str
    right_column_name: str
    ranges: list[tuple[float, float]]
    exceptions: list[int]


class AcTaskResultSchema(BaseTaskResultSchema):
    pass


class AcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left_column_index: int
    right_column_index: int
    left_column_name: str
    right_column_name: str


class AcTaskResultOrderingField(StrEnum):
    LeftColumnIndex = "left_column_index"
    RightColumnIndex = "right_column_index"
    LeftColumnName = "left_column_name"
    RightColumnName = "right_column_name"
    NumberOfRanges = "number_of_ranges"
    NumberOfExceptions = "number_of_exceptions"
