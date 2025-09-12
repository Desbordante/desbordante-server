from enum import StrEnum

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class AfdVerificationRowSchema(BaseSchema):
    row_index: int
    values: list[str]


class AfdVerificationTaskResultItemField(StrEnum):
    NumberOfDistinctRhsValues = "number_of_distinct_rhs_values"
    MostFrequentRhsValueProportion = "most_frequent_rhs_value_proportion"
    Rows = "rows"


class AfdVerificationTaskResultItemSchema(BaseSchema):
    number_of_distinct_rhs_values: int
    most_frequent_rhs_value_proportion: float
    rows: list[AfdVerificationRowSchema]


class AfdVerificationTaskResultSchema(BaseTaskResultSchema):
    afd_holds: bool
    error: float
    number_of_error_clusters: int
    number_of_error_rows: int

    min_number_of_distinct_rhs_values: int | None
    max_number_of_distinct_rhs_values: int | None
    min_most_frequent_rhs_value_proportion: float | None
    max_most_frequent_rhs_value_proportion: float | None


class AfdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    min_number_of_distinct_rhs_values: int
    max_number_of_distinct_rhs_values: int
    min_most_frequent_rhs_value_proportion: float
    max_most_frequent_rhs_value_proportion: float


class AfdVerificationTaskResultOrderingField(StrEnum):
    NumberOfDistinctRhsValues = "number_of_distinct_rhs_values"
    MostFrequentRhsValueProportion = "most_frequent_rhs_value_proportion"
    NumberOfRows = "number_of_rows"
