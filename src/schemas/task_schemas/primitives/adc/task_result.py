from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.adc.types import Operator
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class AdcSideItemSchema(ColumnSchema):
    prefix: str


class AdcItemSchema(BaseSchema):
    lhs_item: AdcSideItemSchema
    rhs_item: AdcSideItemSchema

    operator: Operator


class AdcTaskResultSchema(BaseTaskResultSchema):
    pass


class AdcTaskResultItemField(StrEnum):
    CONJUNCTS = "conjuncts"


class AdcTaskResultItemSchema(BaseSchema):
    conjuncts: list[AdcItemSchema]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_item_names: list[str]
    rhs_item_names: list[str]
    lhs_item_indices: list[int]
    rhs_item_indices: list[int]


class AdcTaskResultOrderingField(StrEnum):
    LHS_ITEM_NAMES = "lhs_item_names"
    RHS_ITEM_NAMES = "rhs_item_names"
    LHS_ITEM_INDICES = "lhs_item_indices"
    RHS_ITEM_INDICES = "rhs_item_indices"
    NUMBER_OF_CONJUNCTS = "number_of_conjuncts"
