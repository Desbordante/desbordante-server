from desbordante.dd.algorithms import Split
from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName, IncorrectAlgorithmName
from internal.domain.task.value_objects.dd import DdTaskConfig, DdTaskResult
from internal.domain.task.value_objects.dd import DdAlgoName, DdModel, DdAlgoResult


class DdTask(Task[Split, DdTaskConfig, DdTaskResult]):
    """
    Task class for discovering Data Dependencies (DD).

    This class handles the execution of the DD algorithm and formats
    the results for further processing.

    Methods:
    - _match_algo_by_name(algo_name: DdAlgoName) -> Split:
      Match the DD algorithm by its name.
    - _collect_result(algo: Split) -> DdTaskResult:
      Process the output of the DD algorithm and return the result.
    """

    def _collect_result(self, algo: Split) -> DdTaskResult:
        """
        Collect and process the DD result.

        Args:
            algo (Split): DD algorithm instance to process.
        Returns:
            DdTaskResult: The processed result containing data dependencies.
        """
        dds = algo.get_dds()
        algo_result = DdAlgoResult(dds=[DdModel.from_dd(dd) for dd in dds])
        return DdTaskResult(primitive_name=PrimitiveName.dd, result=algo_result)

    def _match_algo_by_name(self, algo_name: str) -> Split:
        """
        Match the DD algorithm by name.

        Args:
            algo_name (DdAlgoName): The name of the DD algorithm.
        Returns:
            Split: The corresponding algorithm instance.
        """
        match algo_name:
            case DdAlgoName.Split:
                return Split()
            case _:
                raise IncorrectAlgorithmName(algo_name, "DD")
