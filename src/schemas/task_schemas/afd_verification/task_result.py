from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema


class AfdClusterSchema(BaseSchema):
    num_distinct_rhs_values: int
    most_frequent_rhs_value_proportion: float
    rows: list[list[str]]


class AfdVerificationSchema(BaseSchema):
    error: float  # threshold
    num_error_clusters: int
    num_error_rows: int
    clusters: list[AfdClusterSchema]
    table_header: list[str]
    lhs_rhs_indices: list[int]


class AfdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class AfdVerificationTaskResultOrderingField(StrEnum):
    pass
