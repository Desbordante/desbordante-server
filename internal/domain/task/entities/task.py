from abc import ABC, abstractmethod
import desbordante
import pandas
from internal.domain.task.value_objects import TaskConfig
from internal.domain.task.value_objects import TaskResult


class Task[C: TaskConfig, R: TaskResult](ABC):
    @abstractmethod
    def _match_algo_by_name(self, algo_name) -> desbordante.Algorithm: ...

    @abstractmethod
    def _collect_result(self, algo) -> R: ...

    def execute(self, table: pandas.DataFrame, task_config: C) -> R:
        algo_config = task_config.config
        options = algo_config.model_dump(exclude_unset=True, exclude={"algo_name"})
        algo = self._match_algo_by_name(algo_config.algo_name)
        algo.load_data(table=table)
        algo.execute(**options)
        return self._collect_result(algo)
