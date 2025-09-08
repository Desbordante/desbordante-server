from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class NarSideItemSchema(BaseSchema):
    name: str
    values: str


class NarTaskResultItemSchema(BaseSchema):
    lhs: list[NarSideItemSchema]
    rhs: list[NarSideItemSchema]
    confidence: float
    support: float


class NarTaskResultSchema(BaseTaskResultSchema):
    pass


class NarTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class NarTaskResultOrderingField(StrEnum):
    NumberOfLhs = "number_of_lhs"
    NumberOfRhs = "number_of_rhs"
    Lhs = "lhs"
    Rhs = "rhs"
    Confidence = "confidence"
    Support = "support"
