from typing import Literal, assert_never

import pandas
from desbordante.fd import FdAlgorithm
from desbordante.pfd.algorithms import PFDTane

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.pfd.algo_config import OneOfPfdAlgoConfig
from app.domain.task.schemas.pfd.algo_name import PfdAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class PfdModel(BaseSchema):
    lhs: list[str]
    rhs: list[str]


class BasePfdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.PFD]


class PfdTaskConfig(BasePfdTaskModel):
    config: OneOfPfdAlgoConfig


class PfdTaskResult(BasePfdTaskModel):
    result: list[PfdModel]
    table_header: list[str]


class PfdTask(BaseTask[PfdTaskConfig, PfdTaskResult]):
    _algo_map = {
        PfdAlgoName.PFDTane: PFDTane,
    }

    def match_algo_by_name(self, algo_name: PfdAlgoName) -> FdAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: PfdTaskConfig
    ) -> PfdTaskResult:
        table = tables[0]
        columns = table.columns
        algo_config = task_config["config"]
        options = PfdTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )

        # no limit
        if options['max_lhs'] == 0:
            del options['max_lhs']

        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options)

        return PfdTaskResult(
            primitive_name=PrimitiveName.PFD,
            table_header=columns,
            result=[
                PfdModel(lhs=[columns[index] for index in fd.lhs_indices], rhs=[columns[fd.rhs_index]])
                for fd in algo.get_fds()
            ],
        )
