from pydantic import BaseModel
from desbordante.ac import ACRanges, ACException


class AcModel(BaseModel):
    @classmethod
    def from_ac_range(cls, ac_range: ACRanges):
        return cls(column_indices=ac_range.column_indices, ranges=ac_range.ranges)

    column_indices: tuple[int, int]
    ranges: list[tuple[float, float]]


class AcExceptionModel(BaseModel):
    @classmethod
    def from_ac_exception(cls, ac_exception: ACException):
        return cls(
            row_index=ac_exception.row_index, column_pairs=ac_exception.column_pairs
        )

    row_index: int
    column_pairs: list[tuple[int, int]]


class AcAlgoResult(BaseModel):
    ranges: list[AcModel]
    exceptions: list[AcExceptionModel]
