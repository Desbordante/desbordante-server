from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.adc.types import Operator
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AdcItemSchema(BaseSchema):
    left_prefix: str
    left_column: str
    right_prefix: str
    right_column: str
    operator: Operator


class AdcTaskResultSchema(BaseTaskResultSchema):
    pass


class AdcTaskResultItemField(StrEnum):
    Cojuncts = "cojuncts"
    LeftColumns = "left_columns"
    RightColumns = "right_columns"


class AdcTaskResultItemSchema(BaseSchema):
    cojuncts: list[AdcItemSchema]
    left_columns: list[str]
    right_columns: list[str]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left_columns: list[str]
    right_columns: list[str]


class AdcTaskResultOrderingField(StrEnum):
    LeftColumns = "left_columns"
    RightColumns = "right_columns"
    NumberOfConjuncts = "number_of_conjuncts"
