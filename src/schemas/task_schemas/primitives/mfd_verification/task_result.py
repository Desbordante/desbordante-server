import json
from enum import StrEnum
from typing import Any

from pydantic import field_validator

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class HighlightSchema(BaseSchema):
    highlight_index: int
    data_index: int
    furthest_data_index: int
    max_distance: float
    within_limit: bool
    value: list[str]


class MfdVerificationTaskResultItemSchema(BaseSchema):
    cluster_index: int
    cluster_name: list[str]
    max_distance: float
    highlights_count: int
    highlights: list[HighlightSchema]


class MfdVerificationTaskResultSchema(BaseTaskResultSchema):
    mfd_holds: bool


class MfdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    cluster_indices: list[int]

    @field_validator("cluster_indices", mode="before")
    @classmethod
    def parse_json_arrays(cls, value: Any) -> list:
        return json.loads(value) if isinstance(value, str) else value


class MfdVerificationTaskResultOrderingField(StrEnum):
    DataIndex = "data_index"
    FarthestDataIndex = "farthest_data_index"
    MaxDistance = "max_distance"
