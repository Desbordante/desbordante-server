from enum import StrEnum
from typing import Literal

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AdcItemSchema(BaseSchema):
    left_item: str
    right_item: str
    sign: Literal["==", "!=", "<=", ">=", ">", "<"]


class AdcTaskResultSchema(BaseTaskResultSchema):
    pass


class AdcTaskResultItemSchema(BaseSchema):
    cojuncts: list[AdcItemSchema]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class AdcTaskResultOrderingField(StrEnum):
    NumberOfConjuncts = "number_of_conjuncts"
