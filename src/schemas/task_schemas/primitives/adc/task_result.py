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
    Conjuncts = "conjuncts"


class AdcTaskResultItemSchema(BaseSchema):
    conjuncts: list[AdcItemSchema]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_item_names: list[str]
    rhs_item_names: list[str]
    lhs_item_indices: list[int]
    rhs_item_indices: list[int]


class AdcTaskResultOrderingField(StrEnum):
    LhsItemNames = "lhs_item_names"
    RhsItemNames = "rhs_item_names"
    LhsItemIndices = "lhs_item_indices"
    RhsItemIndices = "rhs_item_indices"
    NumberOfConjuncts = "number_of_conjuncts"
