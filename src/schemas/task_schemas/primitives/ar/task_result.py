from enum import StrEnum
from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class ArTaskResultItemField(StrEnum):
    LHS_VALUES = "lhs_values"
    RHS_VALUES = "rhs_values"
    SUPPORT = "support"
    CONFIDENCE = "confidence"


class ArTaskResultItemSchema(BaseSchema):
    lhs_values: list[str]
    rhs_values: list[str]
    support: float
    confidence: float


class EmptyArTaskResultSchema(BaseTaskResultSchema):
    has_ars: Literal[False]


class NotEmptyArTaskResultSchema(BaseTaskResultSchema):
    has_ars: Literal[True]
    min_support: float
    max_support: float
    min_confidence: float
    max_confidence: float


ArTaskResultSchema = Annotated[
    Union[EmptyArTaskResultSchema, NotEmptyArTaskResultSchema],
    Field(discriminator="has_ars"),
]


class ArTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_values: list[str]
    rhs_values: list[str]

    min_support: float
    max_support: float
    min_confidence: float
    max_confidence: float


class ArTaskResultOrderingField(StrEnum):
    LHS_VALUES = "lhs_values"
    RHS_VALUES = "rhs_values"
    SUPPORT = "support"
    CONFIDENCE = "confidence"
