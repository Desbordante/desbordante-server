from typing import Literal, assert_never
from pydantic import BaseModel
from desbordante.fd import FdAlgorithm  # This is not a typo
from app.domain.task.abstract_task import Task
from app.domain.task.primitive_name import PrimitiveName
from .config import OneOfAfdConfig
from .result import AfdAlgoResult, FdModel
from .algo_name import AfdAlgoName
from desbordante.afd.algorithms import Pyro, Tane


class BaseAfdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.afd]


class AfdTaskConfig(BaseAfdTaskModel):
    config: OneOfAfdConfig


class AfdTaskResult(BaseAfdTaskModel):
    result: AfdAlgoResult


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
