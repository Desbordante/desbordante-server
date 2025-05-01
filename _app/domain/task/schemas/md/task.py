from typing import Literal, assert_never

import pandas
from desbordante.md import (
    MdAlgorithm,
    LhsSimilarityClassifierDesctription,
    RhsSimilarityClassifierDesctription,
)
from desbordante.md.algorithms import HyMD
from desbordante.md.column_matches import (
    Equality,
    Jaccard,
    MongeElkan,
    Lcs,
    Levenshtein,
    LVNormDateDistance,
    LVNormNumberDistance,
)

from _app.domain.task.schemas.base import BaseTask
from _app.domain.task.schemas.types import PrimitiveName
from _app.schemas.schemas import BaseSchema
from .algo_config import OneOfMdAlgoConfig
from .algo_name import MdAlgoName
from .column_matches import ColumnMatchMetrics


class MdSideItemModel(BaseSchema):
    metrics: str
    left_column: str
    right_column: str
    boundary: float


class MdModel(BaseSchema):
    lhs: list[MdSideItemModel]
    rhs: list[MdSideItemModel]


class BaseMdTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.MD]


class MdTaskConfig(BaseMdTaskModel):
    config: OneOfMdAlgoConfig


class MdTaskResult(BaseMdTaskModel):
    result: list[MdModel]
    table_header: list[str]


class MdTask(BaseTask[MdTaskConfig, MdTaskResult]):
    _algo_map = {
        MdAlgoName.HyMD: HyMD,
    }

    _metrics_map = {
        ColumnMatchMetrics.Equality: Equality,
        ColumnMatchMetrics.Jaccard: Jaccard,
        ColumnMatchMetrics.LVNormNumberDistance: LVNormNumberDistance,
        ColumnMatchMetrics.LVNormDateDistance: LVNormDateDistance,
        ColumnMatchMetrics.Lcs: Lcs,
        ColumnMatchMetrics.MongeElkan: MongeElkan,
        ColumnMatchMetrics.Levenshtein: Levenshtein,
    }

    def match_algo_by_name(self, algo_name: MdAlgoName) -> MdAlgorithm:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def match_metrics_by_name(self, metrics: ColumnMatchMetrics):
        if metrics_class := self._metrics_map.get(metrics):
            return metrics_class
        assert_never(metrics)

    def extract_side(
        self,
        side: list[
            LhsSimilarityClassifierDesctription | RhsSimilarityClassifierDesctription
        ],
    ) -> list[MdSideItemModel]:
        sides = []
        for s in side:
            boundary = s.decision_boundary
            metrics = s.column_match_description.column_match_name
            column1 = s.column_match_description.left_column_description.column_name
            column2 = s.column_match_description.right_column_description.column_name
            sides.append(
                MdSideItemModel(
                    metrics=metrics,
                    left_column=column1,
                    right_column=column2,
                    boundary=boundary,
                )
            )
        return sides

    def execute(
        self, tables: list[pandas.DataFrame], task_config: MdTaskConfig
    ) -> MdTaskResult:
        left_table = tables[0]
        header = left_table.columns
        if len(tables) == 2:
            right_table = tables[1]
            header += right_table.columns
        else:
            right_table = tables[0]

        algo_config = task_config["config"]
        column_matches = algo_config["column_matches"]

        options = MdTaskConfig.model_validate(task_config).config.model_dump(
            exclude_unset=True, exclude={"algo_name", "column_matches"}
        )
        cm_array = []
        for cm in column_matches:
            metrics_class = self.match_metrics_by_name(cm["metrics"])
            del cm["metrics"]
            cm_array.append(metrics_class(**cm))

        algo = self.match_algo_by_name(algo_config["algo_name"])

        algo.load_data(left_table=left_table, right_table=right_table)
        if options["max_cardinality"] == -1:
            del options["max_cardinality"]
        algo.execute(**options, column_matches=cm_array)

        return MdTaskResult(
            primitive_name=PrimitiveName.MD,
            table_header=header,
            result=[
                MdModel(
                    lhs=self.extract_side(md.get_description().lhs),
                    rhs=self.extract_side([md.get_description().rhs]),
                )
                for md in algo.get_mds()
            ],
        )
