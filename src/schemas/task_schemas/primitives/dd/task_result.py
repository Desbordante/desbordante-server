from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class DdSideItemSchema(BaseSchema):
    name: str
    values: str


class DdTaskResultItemSchema(BaseSchema):
    lhs: list[DdSideItemSchema]
    rhs: list[DdSideItemSchema]


class DdTaskResultSchema(BaseTaskResultSchema):
    pass


class DdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class DdTaskResultOrderingField(StrEnum):
    NumberOfLhs = "number_of_lhs"
    NumberOfRhs = "number_of_rhs"
