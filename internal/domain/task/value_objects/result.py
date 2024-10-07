from enum import StrEnum
from typing import Protocol, Any
from pydantic import BaseModel


class TaskResult(Protocol):
    """
    Protocol for task result.

    This protocol enforces that any implementing class must:
    - Have a property `primitive_name` that returns a `StrEnum` representing the task type.
    - Include a `result` field which can be any data type.
    - Use Pydantic's `model_dump` method for serializing the result.
    """

    @property
    def primitive_name(self) -> StrEnum:
        """
        Returns:
            str: The name of the primitive associated with the task result.
        """
        ...

    result: Any

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump
