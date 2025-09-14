from enum import StrEnum, auto

from src.schemas.base_schemas import BaseSchema
from src.schemas.task_schemas.types import PrimitiveName


class BaseTaskResultSchema(BaseSchema):
    total_count: int


class PrimitiveResultSchema[R: BaseSchema, I: BaseSchema](BaseSchema):
    result: R
    items: list[I]


class ColumnSchema(BaseSchema):
    name: str
    index: int


class ColumnField(StrEnum):
    NAME = auto()
    INDEX = auto()


class BaseTaskParams[
    P: PrimitiveName,
    C: BaseSchema,
    D: BaseSchema,
](BaseSchema):
    primitive_name: P
    config: C
    datasets: D
