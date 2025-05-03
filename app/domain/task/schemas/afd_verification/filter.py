from enum import StrEnum, auto
from typing import List, assert_never
from .task import AfdVerificationModel
from app.domain.task.schemas.base import BaseFilter


class AfdVerificationFilterOptions(StrEnum):
    SHOW_LHS_RHS_ONLY = auto()


def show_lhs_rhs_only(
    raw_result: AfdVerificationModel, is_show_lhs_rhs_only: bool
) -> AfdVerificationModel:
    if not is_show_lhs_rhs_only:
        return raw_result

    filtered_clusters = []
    for cluster in raw_result["clusters"]:
        filtered_rows = [
            [row[i] for i in raw_result["lhs_rhs_indices"]] for row in cluster["rows"]
        ]

        cluster["rows"] = filtered_rows
        filtered_clusters.append(cluster)

    raw_result["clusters"] = filtered_clusters
    raw_result["table_header"] = [
        raw_result["table_header"][i] for i in raw_result["lhs_rhs_indices"]
    ]
    return raw_result


class AfdVerificationFilter(BaseFilter):
    _filter_map = {
        AfdVerificationFilterOptions.SHOW_LHS_RHS_ONLY: show_lhs_rhs_only,
    }

    def match_filter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def filter(
        self,
        raw_result: AfdVerificationModel,
        filter_option: AfdVerificationFilterOptions,
        filter_params: List[str],
    ) -> AfdVerificationModel:
        filter = self.match_filter_by_option_name(filter_option)
        filtering_result = filter(raw_result, filter_params)
        return filtering_result
