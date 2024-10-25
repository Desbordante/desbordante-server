from desbordante.ind import IndAlgorithm
from desbordante.ind.algorithms import Faida, Mind, Spider
from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName
from internal.domain.task.value_objects.ind import (
    IndAlgoName,
    IndTaskConfig,
    IndTaskResult,
)
from internal.domain.task.value_objects.ind import IndAlgoResult, IndModel


class IndTask(Task[IndAlgorithm, IndTaskConfig, IndTaskResult]):
    """
    Task class for Inclusion Dependency (IND) profiling.

    This class executes various IND algorithms and processes the results
    into the appropriate format. It implements abstract methods from the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: IndAlgoName) -> IndAlgorithm:
      Match IND algorithm by its name.
    - _collect_result(algo: IndAlgorithm) -> IndTaskResult:
      Process the output of the IND algorithm and return the result.
    """

    def _collect_result(self, algo: IndAlgorithm) -> IndTaskResult:
        """
        Collect and process the IND result.

        Args:
            algo (IndAlgorithm): IND algorithm to process.
        Returns:
            IndTaskResult: Processed result containing INDs.
        """
        inds = algo.get_inds()
        algo_result = IndAlgoResult(inds=[IndModel.from_ind(ind) for ind in inds])
        return IndTaskResult(primitive_name=PrimitiveName.ind, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> IndAlgorithm:
        """
        Match the inclusion dependency algorithm by name.

        Args:
            algo_name (IndAlgoName): Name of the IND algorithm.
        Returns:
            IndAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case IndAlgoName.Faida:
                return Faida()
            case IndAlgoName.Mind:
                return Mind()
            case IndAlgoName.Spider:
                return Spider()
            case _:
                raise IncorrectAlgorithmName(algo_name, "IND")
