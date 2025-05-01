from enum import StrEnum, auto
from typing import assert_never
from .task import HoldsMfdVerificationTaskResult, MfdVerificationModel
from app.domain.task.schemas.base import BaseSorter
from app.domain.task.schemas.types import SortOrder


class MfdVerificationSortOptions(StrEnum):
    POINT_INDEX = auto()
    FURTHEST_POINT_INDEX = auto()
    MAXIMUM_DISTANCE = auto()


def sort_by_max_distance(
    raw_result: MfdVerificationModel, is_reverse: bool
) -> MfdVerificationModel:
    # raw_result.sort(key=json.dumps, reverse=is_reverse)
    return HoldsMfdVerificationTaskResult(mfd_holds=True)


class MfdVerificationSorter(BaseSorter):
    _sorter_map = {
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
        is_reverse = sort_direction == SortOrder.DESC
        sorter = self.match_sorter_by_option_name(sort_option)
        print(raw_result)
        sorted_result = sorter(raw_result, is_reverse=is_reverse)
        return sorted_result
