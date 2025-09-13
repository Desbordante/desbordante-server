from enum import StrEnum


from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class MfdVerificationHighlightField(StrEnum):
    DataIndex = "data_index"
    FurthestDataIndex = "furthest_data_index"
    MaxDistance = "max_distance"
    RhsValues = "rhs_values"
    WithinLimit = "within_limit"


class MfdVerificationHighlightSchema(BaseSchema):
    data_index: int
    furthest_data_index: int
    max_distance: float
    rhs_values: list[str]
    within_limit: bool


class MfdVerificationTaskResultItemField(StrEnum):
    MaxDistance = "max_distance"
    Highlights = "highlights"
    ClusterIndex = "cluster_index"
    LhsValues = "lhs_values"


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
    LhsValues = "lhs_values"
    HighlightsDataIndices = "highlights_data_indices"
    HighlightsFurthestDataIndices = "highlights_furthest_data_indices"
    MaxDistance = "max_distance"
    ClusterIndex = "cluster_index"
