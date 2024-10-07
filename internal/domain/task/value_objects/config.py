from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel


class AlgoConfig(Protocol):
    """
    Protocol for algorithm configuration.

    This protocol enforces that any implementing class must:
    - Have a property `algo_name` that returns a `StrEnum`.
    - Use Pydantic's `model_dump` method for serializing the model.
    """

    @property
    def algo_name(self) -> StrEnum:
        """
        Returns:
            str: The name of the algorithm.
        """
        ...

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump


class TaskConfig(Protocol):
    """
    Protocol for task configuration.

    This protocol enforces that any implementing class must:
    - Have a property `primitive_name` that returns a `StrEnum` representing the task type.
    - Have a property `config` that returns an `AlgoConfig`.
    - Use Pydantic's `model_dump` method for serializing the model.
    """

    @property
    def primitive_name(self) -> StrEnum:
        """
        Returns:
            str: The name of the primitive associated with the task.
        """
        ...

    @property
    def config(self) -> AlgoConfig:
        """
        Returns:
            AlgoConfig: the algorithm configuration associated with the task.
        """
        ...

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump
