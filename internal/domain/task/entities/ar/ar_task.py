from desbordante.ar import ArAlgorithm
from desbordante.ar.algorithms import Apriori
from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName
from internal.domain.task.value_objects.ar import ArTaskConfig, ArTaskResult
from internal.domain.task.value_objects.ar import (
    ArAlgoName,
    ArModel,
    ArAlgoResult,
)


class ArTask(Task[ArAlgorithm, ArTaskConfig, ArTaskResult]):
    """
    Task class for Association Rule (AR) mining.

    This class handles the execution of different AR algorithms and processes
    the results into the appropriate format. It implements the abstract methods
    defined in the Task base class.

    Methods:
    - _match_algo_by_name(algo_name: ArAlgoName) -> ArAlgorithm:
      Match AR algorithm by its name.
    - _collect_result(algo: ArAlgorithm) -> ArTaskResult:
      Process the output of the AR algorithm and return the result.
    """

    def _collect_result(self, algo: ArAlgorithm) -> ArTaskResult:
        """
        Collect and process the AR result.

        Args:
            algo (ArAlgorithm): AR algorithm to process.
        Returns:
            ArTaskResult: The processed result containing association rules.
        """
        ar_ids = algo.get_ar_ids()
        ar_strings = algo.get_ars()
        algo_result = ArAlgoResult(
            ars=list(map(ArModel.from_ar, ar_strings)),
            ar_ids=list(map(ArModel.from_ar_ids, ar_ids)),
        )
        return ArTaskResult(primitive_name=PrimitiveName.ar, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> ArAlgorithm:
        """
        Match the association rule algorithm by name.

        Args:
            algo_name (ArAlgoName): The name of the AR algorithm.
        Returns:
            ArAlgorithm: The corresponding algorithm instance.
        """
        match algo_name:
            case ArAlgoName.Apriori:
                return Apriori()
            case _:
                raise IncorrectAlgorithmName(algo_name, "AR")
