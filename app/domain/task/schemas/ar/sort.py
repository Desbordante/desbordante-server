from enum import StrEnum, auto
from typing import assert_never, cast
from .task import (
    ARModel,
)
from app.domain.task.schemas.base import BaseSorter
from app.domain.task.schemas.types import SortOrder


class ARSortOptions(StrEnum):
    CONFIDENCE = auto()
    LHS_NAME = auto()
    RHS_NAME = auto()



def sort_by_confidence(
    raw_result: list[ARModel], is_reverse: bool
) -> list[ARModel]:
    raw_result.sort(
        key=lambda x: x["confidence"], reverse=is_reverse
    )
    return raw_result


def sort_by_lhs(
    raw_result: list[ARModel], is_reverse: bool
) -> list[ARModel]:
    raw_result.sort(
        key=lambda x: x["left"], reverse=is_reverse
    )
    return raw_result


def sort_by_rhs(
    raw_result: list[ARModel], is_reverse: bool
) -> list[ARModel]:
    raw_result.sort(
        key=lambda x: x["right"], reverse=is_reverse
    )
    return raw_result


class ARSorter(BaseSorter):
    _sorter_map = {
        ARSortOptions.CONFIDENCE: sort_by_confidence,
        ARSortOptions.LHS_NAME: sort_by_lhs,
        ARSortOptions.RHS_NAME: sort_by_rhs,
    }

    def match_sorter_by_option_name(self, option_name):
        if sorter_option := self._sorter_map.get(option_name):
            return sorter_option
        assert_never(sorter_option)

    def sort(
        self,
        raw_result: list[ARModel],
        sort_option: ARSortOptions,
        sort_direction: SortOrder,
    ) -> list[ARModel]:
        is_reverse = sort_direction == SortOrder.DESC
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(
            cast(list[ARModel], raw_result), is_reverse=is_reverse
        )
        return sorted_result
