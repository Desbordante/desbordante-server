from enum import StrEnum, auto

from src.schemas.base_schemas import BaseSchema


class BaseTaskResultSchema(BaseSchema):
    total_count: int


class PrimitiveResultSchema[R: BaseSchema, I: BaseSchema](BaseSchema):
    result: R
    items: list[I]


class ColumnSchema(BaseSchema):
    name: str
    index: int


class ColumnField(StrEnum):
    Name = auto()
    Index = auto()
