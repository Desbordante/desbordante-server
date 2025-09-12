from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.adc.types import Operator
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AdcItemSchema(BaseSchema):
    left_prefix: str
    left_index: int
    left_column: str

    right_prefix: str
    right_index: int
    right_column: str

    operator: Operator


class AdcTaskResultSchema(BaseTaskResultSchema):
    pass


class AdcTaskResultItemField(StrEnum):
    Cojuncts = "cojuncts"
    LeftIndices = "left_indices"
    RightIndices = "right_indices"
    LeftColumns = "left_columns"
    RightColumns = "right_columns"


class AdcTaskResultItemSchema(BaseSchema):
    cojuncts: list[AdcItemSchema]
    left_columns: list[str]
    right_columns: list[str]
    left_indices: list[int]
    right_indices: list[int]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left_columns: list[str]
    right_columns: list[str]
    left_indices: list[int]
    right_indices: list[int]


class AdcTaskResultOrderingField(StrEnum):
    LeftColumns = "left_columns"
    RightColumns = "right_columns"
    LeftIndices = "left_index"
    RightIndices = "right_index"
    NumberOfConjuncts = "number_of_conjuncts"
