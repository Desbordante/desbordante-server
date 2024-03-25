from typing import Literal
from pydantic import BaseModel
from app.domain.task.abstract_task import Task
from typing import assert_never
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
from app.domain.task.fd.algo_name import FdAlgoName
from app.domain.task.primitive_name import PrimitiveName
from .config import OneOfFdAlgoConfig
from .result import FdAlgoResult, FdModel


class BaseFdTaskModel(BaseModel):
    primitive_name: Literal[PrimitiveName.fd]


class FdTaskConfig(BaseFdTaskModel):
    config: OneOfFdAlgoConfig


class FdTaskResult(BaseFdTaskModel):
    result: FdAlgoResult


class FdTask(Task[FdTaskConfig, FdTaskResult]):
    def collect_result(self, algo: FdAlgorithm) -> FdTaskResult:
        fds = algo.get_fds()
        algo_result = FdAlgoResult(fds=list(map(FdModel.from_fd, fds)))
        return FdTaskResult(primitive_name=PrimitiveName.fd, result=algo_result)

    def match_algo_by_name(self, algo_name: FdAlgoName) -> FdAlgorithm:
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
        assert_never(algo_name)
