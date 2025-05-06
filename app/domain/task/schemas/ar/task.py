from typing import Literal, assert_never

import pandas
from desbordante.ar import ArAlgorithm

from app.domain.task.schemas.ar.algo_config import OneOfARAlgoConfig
from app.domain.task.schemas.ar.algo_name import ARAlgoName
from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class ARModel(BaseSchema):
    left: list[str]
    right: list[str]
    support: float
    confidence: float


class ARTaskConfig(BaseSchema):
    primitive_name: Literal[PrimitiveName.AR]
    config: OneOfARAlgoConfig


class ARTaskResult(BaseSchema):
    result: list[ARModel]


class ARTask(
    BaseTask[ARTaskConfig, ARTaskResult]
):
    _algo_map = {
        ARAlgoName.AssosiatioRulesApriori: ArAlgorithm,
    }

    def match_algo_by_name(self, algo_name: ARAlgoName) -> ArAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: ARTaskConfig
    ) -> ARTaskResult:
        table = tables[0]
        options = ARTaskConfig.model_validate(
            task_config
        ).config.model_dump(exclude_unset=True, exclude={"algo_name"})

        algo = ArAlgorithm()
        algo.load_data(table=table)
        algo.execute(**options)

        return ARTaskResult(
            primitive_name=PrimitiveName.AR,
            result=algo.get_ars(),
        )
