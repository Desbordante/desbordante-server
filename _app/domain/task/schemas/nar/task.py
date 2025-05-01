from typing import Literal, assert_never

import pandas
from desbordante.nar import NarAlgorithm
from desbordante.nar.algorithms import DES

from _app.domain.task.schemas.base import BaseTask
from _app.domain.task.schemas.types import PrimitiveName
from _app.schemas.schemas import BaseSchema
from .algo_config import OneOfNarAlgoConfig
from .algo_name import NarAlgoName


class NarSideItemModel(BaseSchema):
    name: str
    values: str


class NarModel(BaseSchema):
    lhs: list[NarSideItemModel]
    rhs: list[NarSideItemModel]
    confidence: float
    support: float


class BaseNarTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.NAR]


class NarTaskConfig(BaseNarTaskModel):
    config: OneOfNarAlgoConfig


class NarTaskResult(BaseNarTaskModel):
    result: list[NarModel]
    table_header: list[str]


class NarTask(BaseTask[NarTaskConfig, NarTaskResult]):
    _algo_map = {
        NarAlgoName.DES: DES,
    }

    def match_algo_by_name(self, algo_name: NarAlgoName) -> NarAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def extract_side(self, side, columns) -> list[NarSideItemModel]:
        return [
            NarSideItemModel(name=columns[column_index], values=str(value))
            for column_index, value in side
        ]

    def execute(
        self, tables: list[pandas.DataFrame], task_config: NarTaskConfig
    ) -> NarTaskResult:
        table = tables[0]
        columns = table.columns
        algo_config = task_config["config"]
        options = NarTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )

        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options)

        return NarTaskResult(
            primitive_name=PrimitiveName.NAR,
            table_header=columns,
            result=[
                NarModel(
                    confidence=nar.confidence,
                    support=nar.support,
                    lhs=self.extract_side(nar.ante.items(), columns),
                    rhs=self.extract_side(nar.cons.items(), columns),
                )
                for nar in algo.get_nars()
            ],
        )
