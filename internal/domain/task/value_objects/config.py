from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel


class AlgoConfig(Protocol):
    @property
    def algo_name(self) -> StrEnum: ...

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump


class TaskConfig(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    @property
    def config(self) -> AlgoConfig: ...

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump
