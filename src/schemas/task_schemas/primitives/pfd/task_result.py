from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class PfdTaskResultItemSchema(BaseSchema):
    lhs: list[str]
    rhs: list[str]


class PfdTaskResultSchema(BaseTaskResultSchema):
    pass


class PfdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class PfdTaskResultOrderingField(StrEnum):
    NumberOfLhs = "number_of_lhs"
    NumberOfRhs = "number_of_rhs"
    Lhs = "lhs"
    Rhs = "rhs"
