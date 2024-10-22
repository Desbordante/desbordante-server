from desbordante.fd import FdAlgorithm  # This is not a typo
from desbordante.afd.algorithms import Pyro, Tane

from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName

from internal.domain.task.value_objects.afd import AfdTaskResult, AfdTaskConfig
from internal.domain.task.value_objects.afd import AfdAlgoName, AfdAlgoResult, FdModel


class AfdTask(Task[FdAlgorithm, AfdTaskConfig, AfdTaskResult]):
    """
    Task class for Approximate Functional Dependency (AFD) profiling.

    This class manages the execution of AFD algorithms and processes
    the results into the appropriate format. It implements the abstract methods
    defined in the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: AfdAlgoName) -> FdAlgorithm:
      Match AFD algorithm by its name.
    - _collect_result(algo: FdAlgorithm) -> AfdTaskResult:
      Process the output of the AFD algorithm and return the result.
    """

    def _collect_result(self, algo: FdAlgorithm) -> AfdTaskResult:
        """
        Collect and process the AFD result.

        Args:
            algo (FdAlgorithm): The executed AFD algorithm.
        Returns:
            AfdTaskResult: The processed result containing approximate functional dependencies.
        """
        fds = algo.get_fds()
        algo_result = AfdAlgoResult(fds=list(map(FdModel.from_fd, fds)))
        return AfdTaskResult(primitive_name=PrimitiveName.afd, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> FdAlgorithm:
        """
        Match the approximate functional dependency algorithm by name.

        Args:
            algo_name (AfdAlgoName): The name of the AFD algorithm.
        Returns:
            FdAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case AfdAlgoName.Pyro:
                return Pyro()
            case AfdAlgoName.Tane:
                return Tane()
            case _:
                raise IncorrectAlgorithmName(algo_name, "AFD")
