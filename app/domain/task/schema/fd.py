from app.domain.task.abstract_task import AbstractTask
from enum import StrEnum, auto
from pydantic import BaseModel, Field
from desbordante.fd import FD, FdAlgorithm
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
from typing import Annotated, Generic, TypeVar
from abc import ABC


class TaskAlgoType(StrEnum):
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


class FDModel(BaseModel):
    @classmethod
    def from_fd(cls, fd: FD):
        return cls(lhs_indices=fd.lhs_indices, rhs_index=fd.rhs_index)

    lhs_indices: list[int]
    rhs_index: int


class FDAlgoResult(BaseModel):
    fds: list[FDModel]


# TODO: replace with 3.12 generics when PEP 695 will be supported by mypy
Conf = TypeVar("Conf", bound=BaseModel)
FDAlgo = TypeVar("FDAlgo", bound=FdAlgorithm)


class FDTask(AbstractTask[FDAlgo, Conf, FDAlgoResult], ABC):
    result_model_cls = FDAlgoResult

    def collect_result(self) -> FDAlgoResult:
        fds = self.algorithm.get_fds()
        return FDAlgoResult(fds=list(map(FDModel.from_fd, fds)))


class AidConfig(BaseModel):
    is_null_equal_null: bool


class DFDConfig(BaseModel):
    is_null_equal_null: bool
    threads: Annotated[int, Field(ge=1, le=8)]


class DepminerConfig(BaseModel):
    is_null_equal_null: bool


class FDepConfig(BaseModel):
    is_null_equal_null: bool


class FUNConfig(BaseModel):
    is_null_equal_null: bool


class FastFDsConfig(BaseModel):
    is_null_equal_null: bool
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]


class FdMineConfig(BaseModel):
    is_null_equal_null: bool


class HyFDConfig(BaseModel):
    is_null_equal_null: bool


class PyroConfig(BaseModel):
    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]
    seed: int


class TaneConfig(BaseModel):
    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]


class AidTask(FDTask[Aid, AidConfig, FDAlgoResult]):
    config_model_cls = AidConfig
    algorithm = Aid()


class DFDTask(FDTask[DFD, DFDConfig, FDAlgoResult]):
    config_model_cls = DFDConfig
    algorithm = DFD()


class DepminerTask(FDTask[Depminer, DepminerConfig, FDAlgoResult]):
    config_model_cls = DepminerConfig
    algorithm = Depminer()


class FDepTask(FDTask[FDep, FDepConfig, FDAlgoResult]):
    config_model_cls = FDepConfig
    algorithm = FDep()


class FUNTask(FDTask[FUN, FUNConfig, FDAlgoResult]):
    config_model_cls = FUNConfig
    algorithm = FUN()


class FastFDsTask(FDTask[FastFDs, FastFDsConfig, FDAlgoResult]):
    config_model_cls = FastFDsConfig
    algorithm = FastFDs()


class FdMineTask(FDTask[FdMine, FdMineConfig, FDAlgoResult]):
    config_model_cls = FdMineConfig
    algorithm = FdMine()


class HyFDTask(FDTask[HyFD, HyFDConfig, FDAlgoResult]):
    config_model_cls = HyFDConfig
    algorithm = HyFD()


class PyroTask(FDTask[Pyro, PyroConfig, FDAlgoResult]):
    config_model_cls = PyroConfig
    algorithm = Pyro()


class TaneTask(FDTask[Tane, TaneConfig, FDAlgoResult]):
    config_model_cls = TaneConfig
    algorithm = Tane()
