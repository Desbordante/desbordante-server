from enum import StrEnum, auto
from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema, FiltersParamsSchema


class AcResultType(StrEnum):
    Range = auto()
    Exception = auto()


class AcRangesSchema(BaseSchema):
    type: Literal[AcResultType.Range]
    left_column_index: int
    right_column_index: int
    left_column_name: str
    right_column_name: str
    ranges: list[tuple[float, float]]


class AcExceptionSchema(BaseSchema):
    type: Literal[AcResultType.Exception]
    column_pairs: list[tuple[int, int]]
    column_pairs_names: list[tuple[str, str]]
    row_index: int


AcSchema = Annotated[
    Union[AcRangesSchema, AcExceptionSchema], Field(discriminator="type")
]


class AcTaskResultFiltersSchema(FiltersParamsSchema):
    type: AcResultType = AcResultType.Range
    left_column_index: int | None = None
    right_column_index: int | None = None
    left_column_name: str | None = None
    right_column_name: str | None = None


class AcTaskResultOrderingField(StrEnum):
    LeftColumnIndex = "left_column_index"
    RightColumnIndex = "right_column_index"
    LeftColumnName = "left_column_name"
    RightColumnName = "right_column_name"
    Ranges = "ranges"
    ColumnPairs = "column_pairs"
    ColumnPairsNames = "column_pairs_names"
    RowIndex = "row_index"
