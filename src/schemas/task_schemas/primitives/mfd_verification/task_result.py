from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class MfdVerificationHighlightField(StrEnum):
    DATA_INDEX = "data_index"
    FURTHEST_DATA_INDEX = "furthest_data_index"
    MAX_DISTANCE = "max_distance"
    RHS_VALUES = "rhs_values"
    WITHIN_LIMIT = "within_limit"


class MfdVerificationHighlightSchema(BaseSchema):
    data_index: int
    furthest_data_index: int
    max_distance: float
    rhs_values: list[str]
    within_limit: bool


class MfdVerificationTaskResultItemField(StrEnum):
    MAX_DISTANCE = "max_distance"
    HIGHLIGHTS = "highlights"
    CLUSTER_INDEX = "cluster_index"
    LHS_VALUES = "lhs_values"


class MfdVerificationTaskResultItemSchema(BaseSchema):
    cluster_index: int
    lhs_values: list[str]
    max_distance: float
    highlights: list[MfdVerificationHighlightSchema]


class MfdVerificationTaskResultSchema(BaseTaskResultSchema):
    mfd_holds: bool


class MfdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    cluster_indices: list[int]


class MfdVerificationTaskResultOrderingField(StrEnum):
    LHS_VALUES = "lhs_values"
    HIGHLIGHTS_DATA_INDICES = "highlights_data_indices"
    HIGHLIGHTS_FURTHEST_DATA_INDICES = "highlights_furthest_data_indices"
    MAX_DISTANCE = "max_distance"
    CLUSTER_INDEX = "cluster_index"
