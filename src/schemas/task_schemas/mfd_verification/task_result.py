import json
from enum import StrEnum
from typing import Annotated, Any, Literal, Union

from pydantic import Field, field_validator

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema


class HighlightSchema(BaseSchema):
    highlight_index: int
    data_index: int
    furthest_data_index: int
    max_distance: float
    within_limit: bool
    value: list[str]


class HighlightsClusterSchema(BaseSchema):
    cluster_index: int
    cluster_name: list[str]
    max_distance: float
    highlights_count: int
    highlights: list[HighlightSchema]


class HoldsMfdVerificationSchema(BaseSchema):
    mfd_holds: Literal[True]


class NotHoldsMfdVerificationSchema(BaseSchema):
    mfd_holds: Literal[False]
    cluster_count: int
    highlights_clusters: list[HighlightsClusterSchema]


MfdVerificationSchema = Annotated[
    Union[HoldsMfdVerificationSchema, NotHoldsMfdVerificationSchema],
    Field(discriminator="mfd_holds"),
]


class MfdVerificationTaskResultsFiltersSchema(FiltersParamsSchema, OptionalSchema):
    cluster_indices: list[int]

    @field_validator("cluster_indices", mode="before")
    @classmethod
    def parse_json_arrays(cls, value: Any) -> list:
        return json.loads(value) if isinstance(value, str) else value


class MfdVerificationTaskResultsOrderingField(StrEnum):
    DataIndex = "data_index"
    FarthestDataIndex = "farthest_data_index"
    MaxDistance = "max_distance"
