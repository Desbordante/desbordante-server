import json
from enum import StrEnum
from typing import Any

from pydantic import TypeAdapter, field_validator

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import (
    BaseTaskResultSchema,
    ColumnSchema,
)

from .types import ColumnMatchMetric


class MdTaskResultSideItemField(StrEnum):
    Metric = "metric"
    LeftColumn = "left_column"
    RightColumn = "right_column"
    Boundary = "boundary"
    MaxInvalidBoundary = "max_invalid_boundary"


class MdSideItemSchema(BaseSchema):
    metric: ColumnMatchMetric
    left_column: ColumnSchema
    right_column: ColumnSchema
    boundary: float
    max_invalid_boundary: float | None


class MdTaskResultItemField(StrEnum):
    LhsItems = "lhs_items"
    RhsItem = "rhs_item"


class MdTaskResultItemSchema(BaseSchema):
    lhs_items: list[MdSideItemSchema]
    rhs_item: MdSideItemSchema


class MdTaskResultSchema(BaseTaskResultSchema):
    pass


class MdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_items_metrics: list[ColumnMatchMetric]
    rhs_item_metrics: list[ColumnMatchMetric]
    show_zeroes: bool

    @field_validator("lhs_items_metrics", "rhs_item_metrics", mode="before")
    @classmethod
    def parse_metrics(cls, value: Any) -> list:
        array = json.loads(value) if isinstance(value, str) else value
        return TypeAdapter(list[ColumnMatchMetric]).validate_python(array)


class MdTaskResultOrderingField(StrEnum):
    NumberOfLhsItems = "number_of_lhs_items"

    LhsItemsMetrics = "lhs_items_metrics"
    LhsItemsBoundaries = "lhs_items_boundaries"

    RhsItemMetric = "rhs_item_metric"
    RhsItemBoundary = "rhs_item_boundary"
