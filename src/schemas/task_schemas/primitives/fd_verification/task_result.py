from enum import StrEnum
from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema, OptionalSchema
from src.schemas.task_schemas.primitives.base_schemas import BaseTaskResultSchema


class FdVerificationRowSchema(BaseSchema):
    row_index: int
    values: list[str]


class FdVerificationTaskResultItemField(StrEnum):
    NUMBER_OF_DISTINCT_RHS_VALUES = "number_of_distinct_rhs_values"
    MOST_FREQUENT_RHS_VALUE_PROPORTION = "most_frequent_rhs_value_proportion"
    ROWS = "rows"


class FdVerificationTaskResultItemSchema(BaseSchema):
    number_of_distinct_rhs_values: int
    most_frequent_rhs_value_proportion: float
    rows: list[FdVerificationRowSchema]


class HoldsFdVerificationTaskResultSchema(BaseTaskResultSchema):
    fd_holds: Literal[True]
    error: Literal[0]
    number_of_error_clusters: Literal[0]
    number_of_error_rows: Literal[0]


class NotHoldsFdVerificationTaskResultSchema(BaseTaskResultSchema):
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


FdVerificationTaskResultSchema = Annotated[
    Union[HoldsFdVerificationTaskResultSchema, NotHoldsFdVerificationTaskResultSchema],
    Field(discriminator="fd_holds"),
]


class FdVerificationTaskResultFiltersSchema(FiltersParamsSchema, OptionalSchema):
    min_num: Annotated[int, Field(description="Minimum number of distinct rhs values")]
    max_num: Annotated[int, Field(description="Maximum number of distinct rhs values")]
    min_prop: Annotated[
        float, Field(description="Minimum most frequent rhs value proportion")
    ]
    max_prop: Annotated[
        float, Field(description="Maximum most frequent rhs value proportion")
    ]


class FdVerificationTaskResultOrderingField(StrEnum):
    NUMBER_OF_DISTINCT_RHS_VALUES = "number_of_distinct_rhs_values"
    MOST_FREQUENT_RHS_VALUE_PROPORTION = "most_frequent_rhs_value_proportion"
    NUMBER_OF_ROWS = "number_of_rows"
