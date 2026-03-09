from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class DdSideItemSchema(ColumnSchema):
    distance_interval: tuple[int, int]


class DdTaskResultItemField(StrEnum):
    LHS_ITEMS = "lhs_items"
    RHS_ITEM = "rhs_item"


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
    NUMBER_OF_LHS_ITEMS = "number_of_lhs_items"
    LHS_ITEMS_NAMES = "lhs_items_names"
    LHS_ITEMS_INDICES = "lhs_items_indices"
    RHS_ITEM_NAMES = "rhs_item_names"
    RHS_ITEM_INDICES = "rhs_item_indices"
