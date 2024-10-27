from abc import ABC, abstractmethod
import desbordante
import pandas
from internal.domain.task.value_objects import PrimitiveName, TaskConfig, TaskResult


class Task[A: desbordante.Algorithm, C: TaskConfig, R: TaskResult](ABC):
    """
    Abstract base class for data profiling tasks.

    This class defines the structure for executing algorithms and processing
    their results. Specific task types, such as functional dependency tasks,
    should inherit from this class and implement the necessary methods.

    Type Parameters:
    - C: TaskConfig - Configuration object that defines the algorithm settings.
    - R: TaskResult - Result object that will store the output of the algorithm.

    Methods:
    - _match_algo_by_name(algo_name): Match the algorithm by its name.
    - _collect_result(algo): Collect and process the result of the algorithm.
    - execute(table: pandas.DataFrame, task_config: C): Execute the task
      on a given table with the provided configuration.
    """

    @abstractmethod
    def _match_algo_by_name(self, algo_name: str) -> A:
        """
        Match and return the algorithm instance based on its name.

        Args:
            algo_name (str): Name of the algorithm to match.
        Returns:
            desbordante.Algorithm: Algorithm instance.
        """
        pass

    @abstractmethod
    def _collect_result(self, algo: A) -> R:
        """
        Collect and process the result from the executed algorithm.

        Args:
            algo (desbordante.Algorithm): Algorithm instance.
        Returns:
            TaskResult: The task result containing the processed output.
        """
        pass

    def execute(self, table: pandas.DataFrame, task_config: C) -> R:
        """
        Execute the algorithm on the provided data table.

        Args:
            table (pandas.DataFrame): Data to be processed.
            task_config (TaskConfig): Configuration object that defines the algorithm settings.
        Returns:
            TaskResult: The task result containing the processed output.
        """
        algo_config = task_config.config
        options = algo_config.model_dump(exclude_unset=True, exclude={"algo_name"})
        algo = self._match_algo_by_name(algo_config.algo_name)

        # TODO: FIX THIS PLS!!!
        match task_config.primitive_name:
            case PrimitiveName.ind | PrimitiveName.aind:
                algo.load_data(tables=[table])
            case PrimitiveName.ar:
                algo.load_data(table=table, input_format=options["input_format"])
            case _:
                algo.load_data(table=table)

        algo.execute(**options)
        return self._collect_result(algo)
