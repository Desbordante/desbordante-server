from enum import StrEnum


from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema


class DdSideItemSchema(BaseSchema):
    name: str
    values: str


class DdSchema(BaseSchema):
    lhs: list[DdSideItemSchema]
    rhs: list[DdSideItemSchema]


class DdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class DdTaskResultOrderingField(StrEnum):
    NumberOfLhs = "number_of_lhs"
    NumberOfRhs = "number_of_rhs"
