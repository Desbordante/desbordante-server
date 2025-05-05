from enum import StrEnum, auto
from typing import assert_never, cast, Callable, Union
from copy import deepcopy
from .task import (
    Highlight,
    HighlightsCluster,
    HoldsMfdVerificationTaskResult,
    MfdVerificationModel,
    NotHoldsMfdVerificationTaskResult,
)
from app.domain.task.schemas.base import BaseSorter
from app.domain.task.schemas.types import SortOrder


class MfdVerificationSortOptions(StrEnum):
    DATA_INDEX = auto()
    FURTHEST_DATA_INDEX = auto()
    MAXIMUM_DISTANCE = auto()


def sort_highlights_clusters_but_save_indices_order(
    cluster_count: int,
    highlights_clusters: list[HighlightsCluster],
    is_reverse: bool,
    sort_fun: Callable[[Highlight], Union[int, float]],
) -> list[HighlightsCluster]:
    new_highlights_clusters: list[HighlightsCluster] = []
    for cluster in highlights_clusters:
        sorted_highlights = sorted(
            deepcopy(cluster.highlights),
            key=lambda highlight: (
                sort_fun(highlight),
                highlight.highlight_index * (-1 if is_reverse else 1),
            ),
            reverse=is_reverse,
        )
        new_highlights_clusters.append(
            HighlightsCluster(
                cluster_index=cluster.cluster_index,
                cluster_name=cluster.cluster_name,
                max_distance=cluster.max_distance,
                highlights_count=len(sorted_highlights),
                highlights=sorted_highlights,
            )
        )
    return NotHoldsMfdVerificationTaskResult(
        mfd_holds=False,
        cluster_count=cluster_count,
        highlights_clusters=new_highlights_clusters,
    )


def sort_by_point_index(
    raw_result: NotHoldsMfdVerificationTaskResult, is_reverse: bool
) -> NotHoldsMfdVerificationTaskResult:
    return sort_highlights_clusters_but_save_indices_order(
        raw_result.cluster_count,
        cast(list[HighlightsCluster], raw_result.highlights_clusters),
        is_reverse,
        lambda highlight: highlight.data_index,
    )


def sort_by_furthest_point_index(
    raw_result: NotHoldsMfdVerificationTaskResult, is_reverse: bool
) -> NotHoldsMfdVerificationTaskResult:
    return sort_highlights_clusters_but_save_indices_order(
        raw_result.cluster_count,
        cast(list[HighlightsCluster], raw_result.highlights_clusters),
        is_reverse,
        lambda highlight: highlight.furthest_data_index,
    )


def sort_by_max_distance(
    raw_result: NotHoldsMfdVerificationTaskResult, is_reverse: bool
) -> NotHoldsMfdVerificationTaskResult:
    return sort_highlights_clusters_but_save_indices_order(
        raw_result.cluster_count,
        cast(list[HighlightsCluster], raw_result.highlights_clusters),
        is_reverse,
        lambda highlight: highlight.max_distance,
    )


class MfdVerificationSorter(BaseSorter):
    _sorter_map = {
        MfdVerificationSortOptions.DATA_INDEX: sort_by_point_index,
        MfdVerificationSortOptions.FURTHEST_DATA_INDEX: sort_by_furthest_point_index,
        MfdVerificationSortOptions.MAXIMUM_DISTANCE: sort_by_max_distance,
    }

    def match_sorter_by_option_name(self, option_name):
        if sorter_option := self._sorter_map.get(option_name):
            return sorter_option
        assert_never(sorter_option)

    def sort(
        self,
        raw_result: MfdVerificationModel,
        sort_option: MfdVerificationSortOptions,
        sort_direction: SortOrder,
    ) -> MfdVerificationModel:
        if raw_result.mfd_holds:
            return cast(
                HoldsMfdVerificationTaskResult,
                raw_result,
            )

        is_reverse = sort_direction == SortOrder.DESC
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(
            cast(NotHoldsMfdVerificationTaskResult, raw_result), is_reverse=is_reverse
        )
        return sorted_result
