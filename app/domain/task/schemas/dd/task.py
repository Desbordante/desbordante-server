from typing import Literal, assert_never

import pandas
from desbordante.dd.algorithms import Split

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.dd.algo_config import OneOfDdAlgoConfig
from app.domain.task.schemas.dd.algo_name import DdAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class DdSideItemModel(BaseSchema):
    name: str
    values: str


class DdModel(BaseSchema):
    lhs: list[DdSideItemModel]
    rhs: list[DdSideItemModel]


class BaseDdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.DD]


class DdTaskConfig(BaseDdTaskModel):
    config: OneOfDdAlgoConfig


class DdTaskResult(BaseDdTaskModel):
    result: list[DdModel]
    table_header: list[str]
    count_results: int


class DdTask(BaseTask[DdTaskConfig, DdTaskResult]):
    _algo_map = {
        DdAlgoName.Split: Split,
    }

    def match_algo_by_name(self, algo_name: DdAlgoName) -> Split:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def split_side(self, raw: list[str]) -> list[DdSideItemModel]:
        ans = []
        for s in raw:
            name, value = s.split(" [")
            value = "[" + value
            ans.append(DdSideItemModel(name=name, values=value))
        return ans

    def split_result(self, row: str) -> DdModel:
        lhs_rawraw, rhs_raw = row.split(" -> ")
        lhs_raw = lhs_rawraw.split(" ; ")
        lhs_ans = self.split_side(lhs_raw)
        rhs_ans = self.split_side([rhs_raw])
        return DdModel(lhs=lhs_ans, rhs=rhs_ans)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: DdTaskConfig
    ) -> DdTaskResult:
        table = tables[0]
        table_header = table.columns
        dif_table = tables[1]
        algo_config = task_config["config"]
        options = DdTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )
        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options, difference_table=dif_table)

        task_results = [self.split_result(str(dd)) for dd in algo.get_dds()]
        return DdTaskResult(
            primitive_name=PrimitiveName.DD,
            table_header=table_header,
            result=task_results,
            count_results=len(task_results),
        )
