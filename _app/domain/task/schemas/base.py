from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Protocol

import desbordante
import pandas

from _app.schemas.schemas import BaseSchema


class BaseAlgoConfig(Protocol):
    @property
    def algo_name(self) -> StrEnum: ...

    # forces to use pydantic classes there
    model_dump = BaseSchema.model_dump


class BaseTaskConfig(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    @property
    def config(self) -> BaseAlgoConfig: ...

    # forces to use pydantic classes there
    model_dump = BaseSchema.model_dump


class BaseTaskResult(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    result: Any

    # forces to use pydantic classes there
    model_dump = BaseSchema.model_dump


class BaseTask[C: BaseTaskConfig, R: BaseTaskResult](ABC):
    @abstractmethod
    def match_algo_by_name(self, algo_name) -> desbordante.Algorithm: ...

    @abstractmethod
    def execute(self, tables: list[pandas.DataFrame], task_config: C) -> R: ...


class BaseFilter[R: BaseTaskResult](ABC):
    @abstractmethod
    def match_filter_by_option_name(self, algo_name): ...

    @abstractmethod
    def filter(self, algo_name) -> R: ...


class BaseSorter(ABC):
    @abstractmethod
    def match_sorter_by_option_name(self, algo_name): ...

    @abstractmethod
    def sort(self, algo_name): ...
