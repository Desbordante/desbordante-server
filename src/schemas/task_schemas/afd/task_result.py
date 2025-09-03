from enum import StrEnum

from src.schemas.base_schemas import BaseSchema


class AfdSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str


class AfdTaskResultFiltersSchema(BaseSchema):
    afd_test_filter: bool | None = None


class AfdTaskResultOrderingField(StrEnum):
    LhsIndices = "lhs_indices"
    LhsNames = "lhs_names"
    RhsIndex = "rhs_index"
    RhsName = "rhs_name"
