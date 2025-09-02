from typing import Literal

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.types import PrimitiveName


class AfdModel(BaseSchema):
    lhs: list[str]
    rhs: list[str]


class AfdTaskResult(BaseSchema):
    primitive_name: Literal[PrimitiveName.AFD]
    result: list[AfdModel]
    total_count: int
