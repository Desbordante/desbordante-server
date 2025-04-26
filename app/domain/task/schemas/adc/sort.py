from enum import StrEnum, auto
from typing import List, assert_never
from .task import AdcModel
from app.domain.task.schemas.base import BaseSorter
from app.domain.task.schemas.types import SortOrder
import json


class AdcSortOptions(StrEnum):
    ATTRUBITES_NAMES = auto()
    LEN = auto()

def sort_by_attributes(raw_result: List[AdcModel], 
                       is_reverse: bool) -> List[AdcModel]:
    raw_result.sort(key=json.dumps,
                    reverse=is_reverse)
    return raw_result

def sort_by_len(raw_result: List[AdcModel], 
                      is_reverse: bool) -> List[AdcModel]:
    raw_result.sort(key=lambda x: len(x['cojuncts']),
                    reverse=is_reverse)
    return raw_result





class AdcSorter(BaseSorter):
    _sorter_map = {
        AdcSortOptions.ATTRUBITES_NAMES: sort_by_attributes,   
        AdcSortOptions.LEN: sort_by_len,
        }

    def match_sorter_by_option_name(self, option_name):
        if sorter_option := self._sorter_map.get(option_name):
            return sorter_option
        assert_never(sorter_option)

    def sort(self, 
               raw_result: List[AdcModel],
               sort_option: AdcSortOptions, 
               sort_direction: SortOrder) -> List[AdcModel]:

        is_reverse = sort_direction == SortOrder.DESC 
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(raw_result, is_reverse=is_reverse)
        return sorted_result

