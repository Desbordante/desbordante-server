from enum import StrEnum
from typing import Annotated, Literal, Union

from pydantic import Field

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


class HoldsAfdVerificationTaskResultSchema(BaseTaskResultSchema):
    fd_holds: Literal[True]
    error: Literal[0]
    number_of_error_clusters: Literal[0]
    number_of_error_rows: Literal[0]


class NotHoldsAfdVerificationTaskResultSchema(BaseTaskResultSchema):
    fd_holds: Literal[False]
    error: float
    number_of_error_clusters: int
    number_of_error_rows: int

    min_num: Annotated[int, Field(description="Minimum number of distinct rhs values")]
    max_num: Annotated[int, Field(description="Maximum number of distinct rhs values")]
    min_prop: Annotated[
        float, Field(description="Minimum most frequent rhs value proportion")
    ]
    max_prop: Annotated[
        float, Field(description="Maximum most frequent rhs value proportion")
    ]


AfdVerificationTaskResultSchema = Annotated[
    Union[
        HoldsAfdVerificationTaskResultSchema, NotHoldsAfdVerificationTaskResultSchema
    ],
    Field(discriminator="fd_holds"),
]


class AfdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    min_num: Annotated[int, Field(description="Minimum number of distinct rhs values")]
    max_num: Annotated[int, Field(description="Maximum number of distinct rhs values")]
    min_prop: Annotated[
        float, Field(description="Minimum most frequent rhs value proportion")
    ]
    max_prop: Annotated[
        float, Field(description="Maximum most frequent rhs value proportion")
    ]


class AfdVerificationTaskResultOrderingField(StrEnum):
    NumberOfDistinctRhsValues = "number_of_distinct_rhs_values"
    MostFrequentRhsValueProportion = "most_frequent_rhs_value_proportion"
    NumberOfRows = "number_of_rows"
