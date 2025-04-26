from typing import Literal, assert_never

import pandas
from desbordante.ac import ACRanges, ACException
from desbordante.ac.algorithms import AcAlgorithm

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.ac.algo_config import OneOfAcAlgoConfig, OperationType
from app.domain.task.schemas.ac.algo_name import AcAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class AcModel(BaseSchema):
    left_column: str
    right_column: str
    intervals: list[tuple[float, float]]
    outliers: list[int]

class BaseAcTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.AC]


class AcTaskConfig(BaseAcTaskModel):
    config: OneOfAcAlgoConfig


class AcTaskResult(BaseAcTaskModel):
    operation: OperationType
    result: list[AcModel]
    table_header: list[str]


class AcTask(BaseTask[AcTaskConfig, AcTaskResult]):
    _algo_map = {
        AcAlgoName.BHUNT: AcAlgorithm,
    }

    def match_algo_by_name(self, algo_name: AcAlgoName) -> AcAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def union_result(self, column_names: list[str], 
                     ranges: list[ACRanges], 
                     exceptions: list[ACException]) -> list[AcModel]:
        result = []
        new_exceptions = self.extract_exceptions(exceptions)
        for range in ranges:
            columns = range.column_indices
            result.append(AcModel(
                left_column=column_names[columns[0]],
                right_column=column_names[columns[1]],
                intervals=range.ranges,
                outliers=new_exceptions.setdefault(columns, [])
            ))
        return result
    
    def extract_exceptions(self, exceptions: list[ACException]):
        columns_dict = dict()
        for ex in exceptions:
            for col in ex.column_pairs:
                if col not in columns_dict:
                    columns_dict[col] = []
                columns_dict[col].append(ex.row_index)
        return columns_dict

    def execute(
        self, tables: list[pandas.DataFrame], task_config: AcTaskConfig
    ) -> AcTaskResult:
        table = tables[0]
        column_names = table.columns

        algo_config = task_config["config"]
        options = AcTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name"}
        )

        algo = self.match_algo_by_name(algo_config["algo_name"])
        algo.load_data(table=table)
        algo.execute(**options)

        ac_ranges = algo.get_ac_ranges()
        ac_exceptions = algo.get_ac_exceptions()

        return AcTaskResult(
            primitive_name=PrimitiveName.AC,
            operation=options['bin_operation'],
            table_header=column_names,
            result=self.union_result(column_names, ac_ranges, ac_exceptions),
        )
