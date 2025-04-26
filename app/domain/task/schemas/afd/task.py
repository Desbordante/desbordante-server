from typing import Literal, assert_never

import pandas
from desbordante.fd import FdAlgorithm
from desbordante.fd.algorithms import (
    Pyro,
    Tane,
)

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.afd.algo_config import OneOfAfdAlgoConfig
from app.domain.task.schemas.afd.algo_name import AfdAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class AfdModel(BaseSchema):
    lhs: list[str]
    rhs: list[str]


class BaseAfdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.AFD]


class AfdTaskConfig(BaseAfdTaskModel):
    config: OneOfAfdAlgoConfig


class AfdTaskResult(BaseAfdTaskModel):
    result: list[AfdModel]
    table_header: list[str]


class AfdTask(BaseTask[AfdTaskConfig, AfdTaskResult]):
    _algo_map = {
        AfdAlgoName.Pyro: Pyro,
        AfdAlgoName.Tane: Tane,
    }

    def match_algo_by_name(self, algo_name: AfdAlgoName) -> FdAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: AfdTaskConfig
    ) -> AfdTaskResult:
        table = tables[0]
        columns = table.columns
        algo_config = task_config["config"]
        options = AfdTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )

        # no limit
        if options['max_lhs'] == 0:
            del options['max_lhs']

        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options)

        return AfdTaskResult(
            primitive_name=PrimitiveName.AFD,
            table_header=columns,
            result=[
                AfdModel(lhs=[columns[index] for index in fd.lhs_indices], rhs=[columns[fd.rhs_index]])
                for fd in algo.get_fds()
            ],
        )
