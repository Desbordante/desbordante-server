from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema


class PfdSchema(BaseSchema):
    lhs: list[str]
    rhs: list[str]


class PfdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class PfdTaskResultOrderingField(StrEnum):
    NumberOfLhs = "number_of_lhs"
    NumberOfRhs = "number_of_rhs"
    Lhs = "lhs"
    Rhs = "rhs"
