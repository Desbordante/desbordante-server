from typing import Literal, assert_never

import pandas
from desbordante.ar.algorithms import Apriori

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


class BaseARTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.AR]


class ARTaskConfig(BaseARTaskModel):
    config: OneOfARAlgoConfig


class ARTaskResult(BaseARTaskModel):
    result: list[ARModel]
    count_results: int


class ARTask(BaseTask[ARTaskConfig, ARTaskResult]):
    _algo_map = {
        ARAlgoName.AssosiatioRulesApriori: Apriori,
    }

    def match_algo_by_name(self, algo_name: ARAlgoName) -> Apriori:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: ARTaskConfig
    ) -> ARTaskResult:
        table = tables[0]
        algo_config = task_config["config"]
        options = ARTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name", "input_format"}
        )

        algo = Apriori()
        algo.load_data(table=table, input_format=algo_config["input_format"])
        algo.execute(**options)

        task_results = [
            ARModel(
                left=ar.left,
                right=ar.right,
                support=ar.support,
                confidence=ar.confidence,
            )
            for ar in algo.get_ars()
        ]

        return ARTaskResult(
            primitive_name=PrimitiveName.AR,
            result=task_results,
            count_results=len(task_results),
        )
