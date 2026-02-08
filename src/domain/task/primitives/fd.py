from typing import assert_never

from desbordante.fd import FdAlgorithm
from desbordante.fd.algorithms import (
    DFD,
    FUN,
    Aid,
    Depminer,
    FastFDs,
    FDep,
    FdMine,
    HyFD,
    Pyro,
    Tane,
)

from src.domain.task.abstract_task import Task
from src.schemas.task_schemas.primitives.fd import FdTaskConfig, FdTaskResult
from src.schemas.task_schemas.primitives.fd.algo_name import FdAlgoName
from src.schemas.task_schemas.primitives.fd.result import (
    FdAlgoResult,
    FdModel,
)
from src.schemas.task_schemas.types import PrimitiveName


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
