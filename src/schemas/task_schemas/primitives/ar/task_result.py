import json
from enum import StrEnum
from typing import Any

from pydantic import field_validator

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class ArTaskResultItemSchema(BaseSchema):
    left: list[str]
    right: list[str]
    support: float
    confidence: float


class ArTaskResultSchema(BaseTaskResultSchema):
    pass


class ArTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    left: list[str]
    right: list[str]
    min_support: float
    max_support: float
    min_confidence: float
    max_confidence: float

    @field_validator("left", "right", mode="before")
    @classmethod
    def parse_json_arrays(cls, value: Any) -> list:
        return json.loads(value) if isinstance(value, str) else value


class ArTaskResultOrderingField(StrEnum):
    Left = "left"
    Right = "right"
    Support = "support"
    Confidence = "confidence"
