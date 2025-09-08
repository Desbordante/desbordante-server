import json
from enum import StrEnum
from typing import Any

from pydantic import TypeAdapter, field_validator

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema

from .types import ColumnMatchMetrics


class MdSideItemSchema(BaseSchema):
    metrics: str
    left_column: str
    right_column: str
    boundary: float


class MdTaskResultItemSchema(BaseSchema):
    lhs: list[MdSideItemSchema]
    rhs: list[MdSideItemSchema]


class MdTaskResultSchema(BaseTaskResultSchema):
    pass


class MdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    metrics: list[ColumnMatchMetrics]
    show_zeroes: bool

    @field_validator("metrics", mode="before")
    @classmethod
    def parse_metrics(cls, value: Any) -> list:
        array = json.loads(value) if isinstance(value, str) else value
        return TypeAdapter(list[ColumnMatchMetrics]).validate_python(array)


class MdTaskResultOrderingField(StrEnum):
    NumberOfLhs = "number_of_lhs"
    NumberOfRhs = "number_of_rhs"
    Lhs = "lhs"
    Rhs = "rhs"
