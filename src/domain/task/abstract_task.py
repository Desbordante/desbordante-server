from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Protocol
import desbordante
import pandas
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


class TaskResult(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    result: Any

    # forces to use pydantic classes there
    model_dump = BaseModel.model_dump


class Task[C: TaskConfig, R: TaskResult](ABC):
    @abstractmethod
    def match_algo_by_name(self, algo_name) -> desbordante.Algorithm: ...

    @abstractmethod
    def collect_result(self, algo) -> R: ...

    def execute(self, table: pandas.DataFrame, task_config: C) -> R:
        algo_config = task_config.config
        options = algo_config.model_dump(exclude_unset=True, exclude={"algo_name"})
        algo = self.match_algo_by_name(algo_config.algo_name)
        algo.load_data(table=table)
        algo.execute(**options)
        return self.collect_result(algo)
