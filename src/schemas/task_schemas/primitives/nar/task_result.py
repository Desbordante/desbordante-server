from enum import StrEnum
from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)


class NarStringSideItemSchema(ColumnSchema):
    type: Literal["string"]
    values: list[str]


class NarIntegerSideItemSchema(ColumnSchema):
    type: Literal["integer"]
    range: tuple[int, int]


class NarFloatSideItemSchema(ColumnSchema):
    type: Literal["float"]
    range: tuple[float, float]


NarSideItemSchema = Annotated[
    Union[NarStringSideItemSchema | NarIntegerSideItemSchema | NarFloatSideItemSchema],
    Field(discriminator="type"),
]


class NarTaskResultItemField(StrEnum):
    LHS_ITEMS = "lhs_items"
    RHS_ITEMS = "rhs_items"
    CONFIDENCE = "confidence"
    SUPPORT = "support"
    FITNESS = "fitness"


class NarTaskResultItemSchema(BaseSchema):
    lhs_items: list[NarSideItemSchema]
    rhs_items: list[NarSideItemSchema]
    confidence: float
    support: float
    fitness: float


class NarTaskResultSchema(BaseTaskResultSchema):
    pass


class NarTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    min_confidence: float
    max_confidence: float
    min_support: float
    max_support: float
    min_fitness: float
    max_fitness: float
    lhs_items_names: list[str]
    rhs_items_names: list[str]
    lhs_items_indices: list[int]
    rhs_items_indices: list[int]


class NarTaskResultOrderingField(StrEnum):
    NUMBER_OF_LHS_ITEMS = "number_of_lhs_items"
    NUMBER_OF_RHS_ITEMS = "number_of_rhs_items"
    LHS_ITEMS_NAMES = "lhs_items_names"
    LHS_ITEMS_INDICES = "lhs_items_indices"
    RHS_ITEMS_NAMES = "rhs_items_names"
    RHS_ITEMS_INDICES = "rhs_items_indices"
    CONFIDENCE = "confidence"
    SUPPORT = "support"
    FITNESS = "fitness"
