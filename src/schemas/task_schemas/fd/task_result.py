from typing import Literal

from src.schemas.base_schemas import BaseSchema


class FdSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str


class FdTaskResultFiltersSchema(BaseSchema):
    fd_test_filter: bool | None = None


FdTaskResultOrderingField = Literal["lhs_indices", "lhs_names", "rhs_index", "rhs_name"]
