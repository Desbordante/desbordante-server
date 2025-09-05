from enum import StrEnum
from typing import Literal

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema


class AdcItemSchema(BaseSchema):
    left_item: str
    right_item: str
    sign: Literal["==", "!=", "<=", ">=", ">", "<"]


class AdcSchema(BaseSchema):
    cojuncts: list[AdcItemSchema]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class AdcTaskResultOrderingField(StrEnum):
    Length = "length"
