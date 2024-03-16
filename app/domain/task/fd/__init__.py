from .config import (
    AidConfig,
    DFDConfig,
    DepminerConfig,
    FDepConfig,
    FUNConfig,
    FastFDsConfig,
    FdMineConfig,
    HyFDConfig,
    PyroConfig,
    TaneConfig,
)
from .result import FDModel, FDAlgoResult
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
from app.domain.task.abstract_task import AbstractTask, AnyConf
from app.domain.task.task_factory import TaskFactory
from enum import auto, StrEnum


class FDAlgoName(StrEnum):
    Aid = auto()
    DFD = auto()
    Depminer = auto()
    FDep = auto()
    FUN = auto()
    FastFDs = auto()
    FdMine = auto()
    HyFD = auto()
    Pyro = auto()
    Tane = auto()


class FDTask[FDAlgo: FdAlgorithm, Conf: AnyConf](
    AbstractTask[FDAlgo, Conf, FDAlgoResult]
):
    result_model_cls = FDAlgoResult

    def collect_result(self) -> FDAlgoResult:
        fds = self.algo.get_fds()
        return FDAlgoResult(fds=list(map(FDModel.from_fd, fds)))


fd_factory = TaskFactory(FDAlgoName, FDTask)


@fd_factory.register_task(FDAlgoName.Aid)
class AidTask(FDTask[Aid, AidConfig]):
    config_model_cls = AidConfig
    algo = Aid()


@fd_factory.register_task(FDAlgoName.DFD)
class DFDTask(FDTask[DFD, DFDConfig]):
    config_model_cls = DFDConfig
    algo = DFD()


@fd_factory.register_task(FDAlgoName.Depminer)
class DepminerTask(FDTask[Depminer, DepminerConfig]):
    config_model_cls = DepminerConfig
    algo = Depminer()


@fd_factory.register_task(FDAlgoName.FDep)
class FDepTask(FDTask[FDep, FDepConfig]):
    config_model_cls = FDepConfig
    algo = FDep()


@fd_factory.register_task(FDAlgoName.FUN)
class FUNTask(FDTask[FUN, FUNConfig]):
    config_model_cls = FUNConfig
    algo = FUN()


@fd_factory.register_task(FDAlgoName.FastFDs)
class FastFDsTask(FDTask[FastFDs, FastFDsConfig]):
    config_model_cls = FastFDsConfig
    algo = FastFDs()


@fd_factory.register_task(FDAlgoName.FdMine)
class FdMineTask(FDTask[FdMine, FdMineConfig]):
    config_model_cls = FdMineConfig
    algo = FdMine()


@fd_factory.register_task(FDAlgoName.HyFD)
class HyFDTask(FDTask[HyFD, HyFDConfig]):
    config_model_cls = HyFDConfig
    algo = HyFD()


@fd_factory.register_task(FDAlgoName.Pyro)
class PyroTask(FDTask[Pyro, PyroConfig]):
    config_model_cls = PyroConfig
    algo = Pyro()


@fd_factory.register_task(FDAlgoName.Tane)
class TaneTask(FDTask[Tane, TaneConfig]):
    config_model_cls = TaneConfig
    algo = Tane()
