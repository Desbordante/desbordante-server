from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AfdVerificationTaskResultItemSchema(BaseSchema):
    num_distinct_rhs_values: int
    most_frequent_rhs_value_proportion: float
    rows: list[list[str]]


class AfdVerificationTaskResultSchema(BaseTaskResultSchema):
    error: float
    num_error_clusters: int
    num_error_rows: int


class AfdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    pass


class AfdVerificationTaskResultOrderingField(StrEnum):
    pass
