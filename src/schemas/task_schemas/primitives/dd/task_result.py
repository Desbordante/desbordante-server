from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class DdSideItemSchema(ColumnSchema):
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
    lhs_items_names: list[str]
    lhs_items_indices: list[int]
    rhs_item_names: list[str]
    rhs_item_indices: list[int]


class DdTaskResultOrderingField(StrEnum):
    NumberOfLhsItems = "number_of_lhs_items"
    LhsItemsNames = "lhs_items_names"
    LhsItemsIndices = "lhs_items_indices"
    RhsItemNames = "rhs_item_names"
    RhsItemIndices = "rhs_item_indices"
