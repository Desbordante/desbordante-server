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


from internal.domain.task.entities.task import Task
from internal.domain.task.value_objects import PrimitiveName
from internal.domain.task.value_objects.fd import FdTaskConfig, FdTaskResult
from internal.domain.task.value_objects.fd import FdAlgoName, FdModel, FdAlgoResult


class FdTask(Task[FdTaskConfig, FdTaskResult]):
    def _collect_result(self, algo: FdAlgorithm) -> FdTaskResult:
        fds = algo.get_fds()
        algo_result = FdAlgoResult(fds=list(map(FdModel.from_fd, fds)))
        return FdTaskResult(primitive_name=PrimitiveName.fd, result=algo_result)

    def _match_algo_by_name(self, algo_name: FdAlgoName) -> FdAlgorithm:
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
