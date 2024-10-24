from desbordante.ac.algorithms import AcAlgorithm
from desbordante.ac.algorithms import Default

from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName
from internal.domain.task.value_objects.ac import AcTaskConfig, AcTaskResult
from internal.domain.task.value_objects.ac import (
    AcAlgoName,
    AcModel,
    AcAlgoResult,
    AcExceptionModel,
)


class AcTask(Task[AcAlgorithm, AcTaskConfig, AcTaskResult]):
    """
    Task class for Approximate Consistency (AC) profiling.

    This class handles the execution of different AC algorithms and processes
    the results into the appropriate format. It implements the abstract methods
    defined in the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: AcAlgoName) -> AcAlgorithm:
      Match AC algorithm by its name.
    - _collect_result(algo: AcAlgorithm) -> AcTaskResult:
      Process the output of the AC algorithm and return the result.
    """

    def _collect_result(self, algo: AcAlgorithm) -> AcTaskResult:
        """
        Collect and process the AC result.

        Args:
            algo (AcAlgorithm): AC algorithm to process.
        Returns:
            AcTaskResult: The processed result containing AC ranges and exceptions.
        """
        ac_ranges = algo.get_ac_ranges()
        ac_exceptions = algo.get_ac_exceptions()
        algo_result = AcAlgoResult(
            ranges=list(map(AcModel.from_ac_range, ac_ranges)),
            exceptions=list(map(AcExceptionModel.from_ac_exception, ac_exceptions)),
        )
        return AcTaskResult(primitive_name=PrimitiveName.ac, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> AcAlgorithm:
        """
        Match the approximate consistency algorithm by name.

        Args:
            algo_name (AcAlgoName): The name of the AC algorithm.
        Returns:
            AcAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case AcAlgoName.Default:
                return Default()
            case _:
                raise IncorrectAlgorithmName(algo_name, "AC")
