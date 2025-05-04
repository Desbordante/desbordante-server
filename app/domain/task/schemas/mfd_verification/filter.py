from copy import deepcopy
from enum import StrEnum, auto
from typing import assert_never, cast
from app.domain.task.schemas.base import BaseFilter
from app.domain.task.schemas.mfd_verification.task import (
    HoldsMfdVerificationTaskResult,
    MfdVerificationModel,
    NotHoldsMfdVerificationTaskResult,
)


class MfdVerificationFilterOptions(StrEnum):
    CLUSTER_INDEX = auto()


def filter_by_cluster_index(
    raw_result: NotHoldsMfdVerificationTaskResult, cluster_index: int
) -> NotHoldsMfdVerificationTaskResult:
    if (cluster_index < 0) or (cluster_index >= raw_result["cluster_count"]):
        raise ValueError(f"Invalid cluster index: {cluster_index}")

    return NotHoldsMfdVerificationTaskResult(
        mfd_holds=False,
        cluster_count=raw_result["cluster_count"],
        highlights_clusters=[
            deepcopy(raw_result["highlights_clusters"][cluster_index])
        ],
    )


class MfdVerificationFilter(BaseFilter):
    _filter_map = {
        MfdVerificationFilterOptions.CLUSTER_INDEX: filter_by_cluster_index,
    }

    def match_filter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def filter(
        self,
        raw_result: MfdVerificationModel,
        filter_option: MfdVerificationFilterOptions,
        filter_params: int,
    ) -> MfdVerificationModel:
        if raw_result["mfd_holds"]:
            return cast(
                HoldsMfdVerificationTaskResult,
                raw_result,
            )

        filter = self.match_filter_by_option_name(filter_option)
        filtering_result = filter(
            cast(NotHoldsMfdVerificationTaskResult, raw_result), filter_params
        )
        return filtering_result
