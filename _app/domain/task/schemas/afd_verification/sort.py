from enum import StrEnum, auto
from typing import List, assert_never
from .task import AfdClusterModel
from app.domain.task.schemas.base import BaseSorter
from app.domain.task.schemas.types import SortOrder
import json


class AfdVerificationSortOptions(StrEnum):
    NUM_DISTINCT_RHS_VALUES = auto()
    FREQUENTNESS = auto()
    SIZE = auto()

def sort_by_frequentness(raw_result: List[AfdClusterModel], 
                         is_reverse: bool) -> List[AfdClusterModel]:
    raw_result.sort(key=lambda x: x.most_frequent_rhs_value_proportion,
                    reverse=is_reverse)
    return raw_result

def sort_by_size(raw_result: List[AfdClusterModel], 
                is_reverse: bool) -> List[AfdClusterModel]:
    raw_result.sort(key=lambda x: len(x.rows),
                           reverse=is_reverse)
    return raw_result


def sort_by_rhs(raw_result: List[AfdClusterModel], 
                is_reverse: bool) -> List[AfdClusterModel]:
    raw_result.sort(key=lambda x: x.num_distinct_rhs_values,
                    reverse=is_reverse)
    return raw_result




class AfdVerificationSorter(BaseSorter):
    _sorter_map = {
        AfdVerificationSortOptions.FREQUENTNESS: sort_by_frequentness,   
        AfdVerificationSortOptions.NUM_DISTINCT_RHS_VALUES: sort_by_rhs,
        AfdVerificationSortOptions.SIZE: sort_by_size,  }

    def match_sorter_by_option_name(self, option_name):
        if sorter_option := self._sorter_map.get(option_name):
            return sorter_option
        assert_never(sorter_option)

    def sort(self, 
               raw_result: List[AfdClusterModel],
               sort_option: AfdVerificationSortOptions, 
               sort_direction: SortOrder) -> List[AfdClusterModel]:

        is_reverse = sort_direction == SortOrder.DESC 
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(raw_result, is_reverse=is_reverse)
        return sorted_result

