from pydantic import BaseModel, Field
from typing import Annotated


class AidConfig(BaseModel):
    is_null_equal_null: bool


class DFDConfig(BaseModel):
    is_null_equal_null: bool
    threads: Annotated[int, Field(ge=1, le=8)]


class DepminerConfig(BaseModel):
    is_null_equal_null: bool


class FDepConfig(BaseModel):
    is_null_equal_null: bool


class FUNConfig(BaseModel):
    is_null_equal_null: bool


class FastFDsConfig(BaseModel):
    is_null_equal_null: bool
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]


class FdMineConfig(BaseModel):
    is_null_equal_null: bool


class HyFDConfig(BaseModel):
    is_null_equal_null: bool


class PyroConfig(BaseModel):
    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]
    seed: int


class TaneConfig(BaseModel):
    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
