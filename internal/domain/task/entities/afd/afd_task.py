from typing import assert_never
from desbordante.fd import FdAlgorithm  # This is not a typo
from desbordante.afd.algorithms import Pyro, Tane

from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName

from internal.domain.task.value_objects.afd import AfdTaskResult, AfdTaskConfig
from internal.domain.task.value_objects.afd import AfdAlgoName, AfdAlgoResult, FdModel


class AfdTask(Task[AfdTaskConfig, AfdTaskResult]):
    def _collect_result(self, algo: FdAlgorithm) -> AfdTaskResult:
        fds = algo.get_fds()
        algo_result = AfdAlgoResult(fds=list(map(FdModel.from_fd, fds)))
        return AfdTaskResult(primitive_name=PrimitiveName.afd, result=algo_result)

    def _match_algo_by_name(self, algo_name: AfdAlgoName) -> FdAlgorithm:
        match algo_name:
            case AfdAlgoName.Pyro:
                return Pyro()
            case AfdAlgoName.Tane:
                return Tane()
        assert_never(algo_name)
