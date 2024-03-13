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
from typing import TypeVar
from app.domain.task.abstract_task import AbstractTask
from app.domain.task.task_factory import TaskFactory
from app.domain.task.primitive_factory import PrimitiveFactory, PrimitiveName
from abc import ABC
from enum import StrEnum, auto
from pydantic import BaseModel


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


# TODO: replace with 3.12 generics when PEP 695 will be supported by mypy
Conf = TypeVar("Conf", bound=BaseModel)
FDAlgo = TypeVar("FDAlgo", bound=FdAlgorithm)


class FDTask(AbstractTask[FDAlgo, Conf, FDAlgoResult], ABC):
    result_model_cls = FDAlgoResult

    def collect_result(self) -> FDAlgoResult:
        fds = self.algorithm.get_fds()
        return FDAlgoResult(fds=list(map(FDModel.from_fd, fds)))


fd_factory = PrimitiveFactory.register(
    PrimitiveName.fd, TaskFactory[FDAlgoName, FDTask]()
)


@fd_factory.register_task(FDAlgoName.Aid)
class AidTask(FDTask[Aid, AidConfig, FDAlgoResult]):
    config_model_cls = AidConfig
    algorithm = Aid()


@fd_factory.register_task(FDAlgoName.DFD)
class DFDTask(FDTask[DFD, DFDConfig, FDAlgoResult]):
    config_model_cls = DFDConfig
    algorithm = DFD()


@fd_factory.register_task(FDAlgoName.Depminer)
class DepminerTask(FDTask[Depminer, DepminerConfig, FDAlgoResult]):
    config_model_cls = DepminerConfig
    algorithm = Depminer()


@fd_factory.register_task(FDAlgoName.FDep)
class FDepTask(FDTask[FDep, FDepConfig, FDAlgoResult]):
    config_model_cls = FDepConfig
    algorithm = FDep()


@fd_factory.register_task(FDAlgoName.FUN)
class FUNTask(FDTask[FUN, FUNConfig, FDAlgoResult]):
    config_model_cls = FUNConfig
    algorithm = FUN()


@fd_factory.register_task(FDAlgoName.FastFDs)
class FastFDsTask(FDTask[FastFDs, FastFDsConfig, FDAlgoResult]):
    config_model_cls = FastFDsConfig
    algorithm = FastFDs()


@fd_factory.register_task(FDAlgoName.FdMine)
class FdMineTask(FDTask[FdMine, FdMineConfig, FDAlgoResult]):
    config_model_cls = FdMineConfig
    algorithm = FdMine()


@fd_factory.register_task(FDAlgoName.HyFD)
class HyFDTask(FDTask[HyFD, HyFDConfig, FDAlgoResult]):
    config_model_cls = HyFDConfig
    algorithm = HyFD()


@fd_factory.register_task(FDAlgoName.Pyro)
class PyroTask(FDTask[Pyro, PyroConfig, FDAlgoResult]):
    config_model_cls = PyroConfig
    algorithm = Pyro()


@fd_factory.register_task(FDAlgoName.Tane)
class TaneTask(FDTask[Tane, TaneConfig, FDAlgoResult]):
    config_model_cls = TaneConfig
    algorithm = Tane()
