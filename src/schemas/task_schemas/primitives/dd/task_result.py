from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class DdSideItemSchema(BaseSchema):
    column_name: str
    column_index: int
    distance_interval: tuple[int, int]


class DdTaskResultItemField(StrEnum):
    LhsItems = "lhs_items"
    RhsItem = "rhs_item"


class DdTaskResultItemSchema(BaseSchema):
    lhs_items: list[DdSideItemSchema]
    rhs_item: DdSideItemSchema


class DdTaskResultSchema(BaseTaskResultSchema):
    pass


class DdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_column_names: list[str]
    lhs_column_indices: list[int]
    rhs_column_names: list[str]
    rhs_column_indices: list[int]


class DdTaskResultOrderingField(StrEnum):
    NumberOfLhsItems = "number_of_lhs_items"
    LhsColumnNames = "lhs_column_names"
    LhsColumnIndices = "lhs_column_indices"
    RhsColumnNames = "rhs_column_names"
    RhsColumnIndices = "rhs_column_indices"
