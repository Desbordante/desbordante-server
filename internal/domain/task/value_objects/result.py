from enum import StrEnum
from typing import Protocol, Any
from pydantic import BaseModel


class TaskResult(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    result: Any

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump
