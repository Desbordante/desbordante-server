from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.adc.types import Operator
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AdcItemSchema(BaseSchema):
    lhs_prefix: str
    lhs_index: int
    lhs_column: str

    rhs_prefix: str
    rhs_index: int
    rhs_column: str

    operator: Operator


class AdcTaskResultSchema(BaseTaskResultSchema):
    pass


class AdcTaskResultItemField(StrEnum):
    Cojuncts = "cojuncts"
    LhsIndices = "lhs_indices"
    RhsIndices = "rhs_indices"
    LhsColumns = "lhs_columns"
    RhsColumns = "rhs_columns"


class AdcTaskResultItemSchema(BaseSchema):
    cojuncts: list[AdcItemSchema]
    lhs_columns: list[str]
    rhs_columns: list[str]
    lhs_indices: list[int]
    rhs_indices: list[int]


class AdcTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_columns: list[str]
    rhs_columns: list[str]
    lhs_indices: list[int]
    rhs_indices: list[int]


class AdcTaskResultOrderingField(StrEnum):
    LhsColumns = "lhs_columns"
    RhsColumns = "rhs_columns"
    LhsIndices = "lhs_index"
    RhsIndices = "rhs_index"
    NumberOfConjuncts = "number_of_conjuncts"
