from desbordante.cfd import CfdAlgorithm
from desbordante.cfd.algorithms import FDFirst
from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName
from internal.domain.task.value_objects.cfd import CfdTaskConfig, CfdTaskResult
from internal.domain.task.value_objects.cfd import (
    CfdAlgoName,
    CfdModel,
    CfdAlgoResult,
)


class CfdTask(Task[CfdAlgorithm, CfdTaskConfig, CfdTaskResult]):
    """
    Task class for Conditional Functional Dependencies (CFD) mining.

    This class handles the execution of different CFD algorithms and processes
    the results into the appropriate format. It implements the abstract methods
    defined in the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: CfdAlgoName) -> CfdAlgorithm:
      Match CFD algorithm by its name.
    - _collect_result(algo: CfdAlgorithm) -> CfdTaskResult:
      Process the output of the CFD algorithm and return the result.
    """

    def _collect_result(self, algo: CfdAlgorithm) -> CfdTaskResult:
        """
        Collect and process the CFD result.

        Args:
            algo (CfdAlgorithm): CFD algorithm to process.
        Returns:
            CfdTaskResult: The processed result containing CFDs.
        """
        cfds = algo.get_cfds()
        algo_result = CfdAlgoResult(cfds=[CfdModel.from_cfd(cfd) for cfd in cfds])
        return CfdTaskResult(primitive_name=PrimitiveName.cfd, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> CfdAlgorithm:
        """
        Match the CFD algorithm by name.

        Args:
            algo_name (CfdAlgoName): The name of the CFD algorithm.
        Returns:
            CfdAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case CfdAlgoName.FDFirst:
                return FDFirst()
            case _:
                raise IncorrectAlgorithmName(algo_name, "CFD")
