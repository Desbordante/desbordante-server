from typing import Literal

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.types import PrimitiveName


class FdSchema(BaseSchema):
    lhs_indices: list[int]
    rhs_index: int


class FdTaskResult(BaseSchema):
    primitive_name: Literal[PrimitiveName.FD]
    result: list[FdSchema]
    total_count: int
