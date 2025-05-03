from typing import Literal, assert_never

import pandas
from desbordante.dc.algorithms import FastADC

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.adc.algo_config import OneOfAdcAlgoConfig
from app.domain.task.schemas.adc.algo_name import AdcAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class AdcItemModel(BaseSchema):
    left_item: str
    right_item: str
    sign: Literal["==", "!=", "<=", ">=", ">", "<"]


class AdcModel(BaseSchema):
    cojuncts: list[AdcItemModel]


class BaseAdcTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.ADC]


class AdcTaskConfig(BaseAdcTaskModel):
    config: OneOfAdcAlgoConfig


class AdcTaskResult(BaseAdcTaskModel):
    result: list[AdcModel]
    table_header: list[str]


class AdcTask(BaseTask[AdcTaskConfig, AdcTaskResult]):
    _algo_map = {
        AdcAlgoName.FastADC: FastADC,
    }

    def match_algo_by_name(self, algo_name: AdcAlgoName) -> FastADC:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def split_result(self, row: str) -> list[AdcItemModel]:
        row_len = len(row)
        row = row[2 : row_len - 1]
        conjuncts = row.split("∧")
        result = []
        for con in conjuncts:
            left_item, sign, right_item = con.split()
            result.append(
                AdcItemModel(left_item=left_item, sign=sign, right_item=right_item)
            )
        return result

    def execute(
        self, tables: list[pandas.DataFrame], task_config: AdcTaskConfig
    ) -> AdcTaskResult:
        table = tables[0]
        column_names = table.columns

        algo_config = task_config["config"]
        options = AdcTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )

        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options)

        return AdcTaskResult(
            primitive_name=PrimitiveName.ADC,
            table_header=column_names,
            result=[
                AdcModel(cojuncts=self.split_result(str(dc))) for dc in algo.get_dcs()
            ],
        )
