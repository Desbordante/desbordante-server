from typing import assert_never

from desbordante.afd.algorithms import (
    Pyro,
    Tane,
)
from desbordante.fd import FdAlgorithm  # This is not a typo

from src.domain.task.abstract_task import Task
from src.schemas.task_schemas.primitives.afd import AfdTaskConfig, AfdTaskResult
from src.schemas.task_schemas.primitives.afd.algo_name import AfdAlgoName
from src.schemas.task_schemas.primitives.afd.result import AfdAlgoResult, FdModel
from src.schemas.task_schemas.types import PrimitiveName


class AfdTask(Task[AfdTaskConfig, AfdTaskResult]):
    def collect_result(self, algo: FdAlgorithm) -> AfdTaskResult:
        fds = algo.get_fds()
        algo_result = AfdAlgoResult(fds=list(map(FdModel.from_fd, fds)))
        return AfdTaskResult(primitive_name=PrimitiveName.afd, result=algo_result)

    def match_algo_by_name(self, algo_name: AfdAlgoName) -> FdAlgorithm:
        match algo_name:
            case AfdAlgoName.Pyro:
                return Pyro()
            case AfdAlgoName.Tane:
                return Tane()
        assert_never(algo_name)
