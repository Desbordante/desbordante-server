from operator import attrgetter
from typing import Union, Literal, assert_never

import pandas
from desbordante.mfd_verification.algorithms import MetricVerifier

from app.domain.task.schemas.base import BaseTask
from app.domain.task.schemas.mfd_verification.algo_config import (
    OneOfMfdVerificationAlgoConfig,
)
from app.domain.task.schemas.mfd_verification.algo_name import MfdVerificationAlgoName
from app.domain.task.schemas.types import PrimitiveName
from app.schemas.schemas import BaseSchema


class BaseMfdVerificationTaskModel(BaseSchema):
    primitive_name: Literal[PrimitiveName.MFD_VERIFICATION]


class HoldsMfdVerificationTaskResult(BaseSchema):
    mfd_holds: Literal[True]


class Highlight(BaseSchema):
    highlight_index: int
    data_index: int
    furthest_data_index: int
    max_distance: float
    within_limit: bool
    value: list[str]


class HighlightsCluster(BaseSchema):
    cluster_index: int
    cluster_name: list[str]
    max_distance: float
    highlights: list[Highlight]


class NotHoldsMfdVerificationTaskResult(BaseSchema):
    mfd_holds: Literal[False]
    highlights_clusters: list[HighlightsCluster]


class MfdVerificationTaskConfig(BaseMfdVerificationTaskModel):
    config: OneOfMfdVerificationAlgoConfig


class MfdVerificationTaskResult(BaseMfdVerificationTaskModel):
    result: Union[HoldsMfdVerificationTaskResult, NotHoldsMfdVerificationTaskResult]


class MfdVerificationTask(
    BaseTask[MfdVerificationTaskConfig, MfdVerificationTaskResult]
):
    _algo_map = {
        MfdVerificationAlgoName.MetricVerification: MetricVerifier,
    }

    def match_algo_by_name(self, algo_name: MfdVerificationAlgoName) -> MetricVerifier:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        assert_never(algo_name)

    def execute(
        self, tables: list[pandas.DataFrame], task_config: MfdVerificationTaskConfig
    ) -> MfdVerificationTaskResult:
        table = tables[0]
        options = MfdVerificationTaskConfig.model_validate(
            task_config
        ).config.model_dump(exclude_unset=True, exclude={"algo_name"})

        # add verification for options

        algo = MetricVerifier()
        algo.load_data(table=table)
        algo.execute(**options)

        if algo.mfd_holds():
            result = HoldsMfdVerificationTaskResult(mfd_holds=True)
        else:
            hidhlights_clusters: list[HighlightsCluster] = []
            highlights_list = algo.get_highlights()
            for cluster_index, cluster in enumerate(highlights_list):
                # get lhs values of the first row of the cluster
                cluster_name = (
                    list(
                        map(
                            str,
                            table.iloc[
                                [cluster[0].data_index],
                                task_config["config"]["lhs_indices"],
                            ].values[0],
                        )
                    )
                    if len(cluster) > 0
                    else []
                )
                max_distance = max(map(attrgetter("max_distance"), cluster))
                highlights: list[Highlight] = []
                for highlight_index, highlight in enumerate(cluster):
                    # get rhs values of the current row in the cluster
                    value = (
                        list(
                            map(
                                str,
                                table.iloc[
                                    [highlight.data_index],
                                    task_config["config"]["rhs_indices"],
                                ].values[0],
                            )
                        )
                        if len(cluster) > 0
                        else []
                    )
                    highlights.append(
                        Highlight(
                            highlight_index=highlight_index,
                            data_index=highlight.data_index,
                            furthest_data_index=highlight.furthest_data_index,
                            max_distance=highlight.max_distance,
                            within_limit=highlight.max_distance
                            <= task_config["config"]["parameter"],
                            value=value,
                        )
                    )
                hidhlights_clusters.append(
                    HighlightsCluster(
                        cluster_index=cluster_index,
                        cluster_name=cluster_name,
                        max_distance=max_distance,
                        highlights=highlights,
                    )
                )

            result = NotHoldsMfdVerificationTaskResult(
                mfd_holds=False,
                highlights_clusters=hidhlights_clusters,
            )

        return MfdVerificationTaskResult(
            primitive_name=PrimitiveName.MFD_VERIFICATION,
            result=result,
        )
