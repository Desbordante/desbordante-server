from typing import Literal, assert_never

import pandas
from desbordante.dd import DD
from desbordante.dd.algorithms import Split

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.dd.algo_config import OneOfDdAlgoConfig
from app.domain.task.schemas.dd.algo_name import DdAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class DdSideModel(BaseSchema):
    name: str
    values: str


class DdModel(BaseSchema):
    lhs: list[DdSideModel]
    rhs: list[DdSideModel]


class BaseDdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.DD]


class DdTaskConfig(BaseDdTaskModel):
    config: OneOfDdAlgoConfig


class DdTaskResult(BaseDdTaskModel):
    result: list[DdModel]


class DdTask(BaseTask[DdTaskConfig, DdTaskResult]):
    _algo_map = {
        DdAlgoName.Split: Split,
    }

    def match_algo_by_name(self, algo_name: DdAlgoName) -> Split:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    # def extract_side(self, side, columns) -> list[DdSideModel]:
    #     return [
    #         DdSideModel(name=columns[column_index], values=str(value))
    #         for column_index, value in side
    #     ]
        
    def split_side(self, raw: list[str]) -> list[DdSideModel]:
        ans = []
        for s in raw:
            name, value = s.split(' [')
            value = '[' + value
            ans.append({'name': name, 'values': value})
        return ans


    def split_result(self, row: str) -> DdModel:
        lhs_rawraw, rhs_raw = row.split(' -> ')
        lhs_raw = lhs_rawraw.split(' ; ')
        lhs_ans = self.split_side(lhs_raw)
        rhs_ans = self.split_side([rhs_raw])
        # print(111, lhs_ans)
        # print(222, rhs_ans)
        return DdModel(lhs=lhs_ans, rhs=rhs_ans) 
        

    def execute(
        self, tables: list[pandas.DataFrame], task_config: DdTaskConfig
    ) -> DdTaskResult:
        table = tables[0]
        dif_table = tables[1]
        # print(666, tables[1])
        # columns = table.columns
        algo_config = task_config["config"]
        options = DdTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )
        # print(777, options)
        algo = self.match_algo_by_name(algo_config["algo_name"])
        #algo = Split
        algo.load_data(table=table)
        # algo.execute(**options)
        # algo.execute(difference_table=dif_table)
        algo.execute(**options, difference_table=dif_table)

        return DdTaskResult(
            primitive_name=PrimitiveName.DD,
            result=[self.split_result(str(dd)) for dd in algo.get_dds()],
        )
