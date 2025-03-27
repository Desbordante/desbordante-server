from typing import Literal, assert_never

import pandas
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

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.fd.algo_config import OneOfFdAlgoConfig
from app.domain.task.schemas.fd.algo_name import FdAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class FdModel(BaseSchema):
    lhs_indices: list[int]
    rhs_index: int


class BaseFdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.FD]


class FdTaskConfig(BaseFdTaskModel):
    config: OneOfFdAlgoConfig


class FdTaskResult(BaseFdTaskModel):
    result: list[FdModel]


class FdTask(BaseTask[FdTaskConfig, FdTaskResult]):
    _algo_map = {
        FdAlgoName.Aid: Aid,
        FdAlgoName.DFD: DFD,
        FdAlgoName.Depminer: Depminer,
        FdAlgoName.FDep: FDep,
        FdAlgoName.FUN: FUN,
        FdAlgoName.FastFDs: FastFDs,
        FdAlgoName.FdMine: FdMine,
        FdAlgoName.HyFD: HyFD,
        FdAlgoName.Pyro: Pyro,
        FdAlgoName.Tane: Tane,
    }

    def match_algo_by_name(self, algo_name: FdAlgoName) -> FdAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: FdTaskConfig
    ) -> FdTaskResult:
        table = tables[0]
        algo_config = task_config.config
        options = algo_config.model_dump(exclude_unset=True, exclude={"algo_name"})

        algo = self.match_algo_by_name(algo_config.algo_name)
        algo.load_data(table=table)
        algo.execute(**options)

        return FdTaskResult(
            primitive_name=PrimitiveName.FD,
            result=[
                FdModel(lhs_indices=fd.lhs_indices, rhs_index=fd.rhs_index)
                for fd in algo.get_fds()
            ],
        )
