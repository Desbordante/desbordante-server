from pydantic import Field
from typing import Annotated

from app.domain.common.optional_model import OptionalModel


class AidConfig(OptionalModel):
    is_null_equal_null: bool


class DFDConfig(OptionalModel):
    is_null_equal_null: bool
    threads: Annotated[int, Field(ge=1, le=8)]


class DepminerConfig(OptionalModel):
    is_null_equal_null: bool


class FDepConfig(OptionalModel):
    is_null_equal_null: bool


class FUNConfig(OptionalModel):
    is_null_equal_null: bool


class FastFDsConfig(OptionalModel):
    is_null_equal_null: bool
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]


class FdMineConfig(OptionalModel):
    is_null_equal_null: bool


class HyFDConfig(OptionalModel):
    is_null_equal_null: bool


class PyroConfig(OptionalModel):
    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]
    seed: int


class TaneConfig(OptionalModel):
    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
