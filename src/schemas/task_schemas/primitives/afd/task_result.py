import json
from enum import StrEnum
from typing import Any

from pydantic import field_validator

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AfdTaskResultItemSchema(BaseSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str


class AfdTaskResultSchema(BaseTaskResultSchema):
    pass


class AfdTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    lhs_indices: list[int]
    lhs_names: list[str]
    rhs_index: int
    rhs_name: str

    @field_validator("lhs_indices", "lhs_names", mode="before")
    @classmethod
    def parse_json_arrays(cls, value: Any) -> list:
        return json.loads(value) if isinstance(value, str) else value


class AfdTaskResultOrderingField(StrEnum):
    LhsIndices = "lhs_indices"
    LhsNames = "lhs_names"
    RhsIndex = "rhs_index"
    RhsName = "rhs_name"
