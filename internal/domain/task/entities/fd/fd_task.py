from desbordante.fd import FdAlgorithm
from desbordante.fd.algorithms import (
    Aid,
    DFD,
    Depminer,
    FDep,
    FUN,
    FastFDs,
    FdMine,
    HyFD,
    Pyro,
    Tane,
)

from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName
from internal.domain.task.value_objects.fd import FdTaskConfig, FdTaskResult
from internal.domain.task.value_objects.fd import (
    FdAlgoName,
    FdModel,
    FdAlgoResult,
    IncorrectFDAlgorithmName,
)


class FdTask(Task[FdAlgorithm, FdTaskConfig, FdTaskResult]):
    """
    Task class for Functional Dependency (FD) profiling.

    This class handles the execution of different FD algorithms and processes
    the results into the appropriate format. It implements the abstract methods
    defined in the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: FdAlgoName) -> FdAlgorithm:
      Match FD algorithm by its name.
    - _collect_result(algo: FdAlgorithm) -> FdTaskResult:
      Process the output of the FD algorithm and return the result.
    """

    def _collect_result(self, algo: FdAlgorithm) -> FdTaskResult:
        """
        Collect and process the FD result.

        Args:
            algo (FdAlgorithm): FD algorithm to process.
        Returns:
            FdTaskResult: The processed result containing functional dependencies.
        """
        fds = algo.get_fds()
        algo_result = FdAlgoResult(fds=list(map(FdModel.from_fd, fds)))
        return FdTaskResult(primitive_name=PrimitiveName.fd, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> FdAlgorithm:
        """
        Match the functional dependency algorithm by name.

        Args:
            algo_name (FdAlgoName): The name of the FD algorithm.
        Returns:
            FdAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case FdAlgoName.Aid:
                return Aid()
            case FdAlgoName.DFD:
                return DFD()
            case FdAlgoName.Depminer:
                return Depminer()
            case FdAlgoName.FDep:
                return FDep()
            case FdAlgoName.FUN:
                return FUN()
            case FdAlgoName.FastFDs:
                return FastFDs()
            case FdAlgoName.FdMine:
                return FdMine()
            case FdAlgoName.HyFD:
                return HyFD()
            case FdAlgoName.Pyro:
                return Pyro()
            case FdAlgoName.Tane:
                return Tane()
            case _:
                raise IncorrectFDAlgorithmName(algo_name)
