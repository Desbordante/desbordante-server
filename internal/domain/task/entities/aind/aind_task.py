from desbordante.ind import IndAlgorithm
from desbordante.aind.algorithms import Mind, Spider
from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName
from internal.domain.task.value_objects.aind import (
    AindAlgoName,
    AindTaskConfig,
    AindTaskResult,
)
from internal.domain.task.value_objects.aind import AindAlgoResult, AindModel


class AindTask(Task[IndAlgorithm, AindTaskConfig, AindTaskResult]):
    """
    Task class for Inclusion Dependency (AIND) profiling.

    This class executes various AIND algorithms and processes the results
    into the appropriate format. It implements abstract methods from the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: AindAlgoName) -> AindAlgorithm:
      Match AIND algorithm by its name.
    - _collect_result(algo: AindAlgorithm) -> AindTaskResult:
      Process the output of the AIND algorithm and return the result.
    """

    def _collect_result(self, algo: IndAlgorithm) -> AindTaskResult:
        """
        Collect and process the AIND result.

        Args:
            algo (AindAlgorithm): AIND algorithm to process.
        Returns:
            AindTaskResult: Processed result containing AINDs.
        """
        ainds = algo.get_inds()
        algo_result = AindAlgoResult(inds=[AindModel.from_ind(aind) for aind in ainds])
        return AindTaskResult(primitive_name=PrimitiveName.aind, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> IndAlgorithm:
        """
        Match the inclusion dependency algorithm by name.

        Args:
            algo_name (AindAlgoName): Name of the AIND algorithm.
        Returns:
            AindAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case AindAlgoName.Mind:
                return Mind()
            case AindAlgoName.Spider:
                return Spider()
            case _:
                raise IncorrectAlgorithmName(algo_name, "AIND")
