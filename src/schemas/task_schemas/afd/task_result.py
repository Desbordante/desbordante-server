from typing import Literal

from src.schemas.base_schemas import BaseSchema


class AfdSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str


class AfdTaskResultFiltersSchema(BaseSchema):
    afd_test_filter: bool | None = None


AfdTaskResultOrderingField = Literal[
    "lhs_indices", "lhs_names", "rhs_index", "rhs_name"
]
