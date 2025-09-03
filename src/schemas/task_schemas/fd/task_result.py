from enum import StrEnum

from src.schemas.base_schemas import BaseSchema


class FdSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str


class FdTaskResultFiltersSchema(BaseSchema):
    fd_test_filter: bool | None = None


class FdTaskResultOrderingField(StrEnum):
    LhsIndices = "lhs_indices"
    LhsNames = "lhs_names"
    RhsIndex = "rhs_index"
    RhsName = "rhs_name"
