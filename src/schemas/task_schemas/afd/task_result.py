from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema


class AfdSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str


class AfdTaskResultFiltersSchema(FiltersParamsSchema):
    pass


class AfdTaskResultOrderingField(StrEnum):
    LhsIndices = "lhs_indices"
    LhsNames = "lhs_names"
    RhsIndex = "rhs_index"
    RhsName = "rhs_name"
