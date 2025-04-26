from enum import StrEnum, auto
from typing import List, assert_never
from .task import AcModel
from app.domain.task.schemas.base import BaseSorter
from app.domain.task.schemas.types import SortOrder
import json


class AcSortOptions(StrEnum):
    ATTRUBITES_NAMES = auto()
    NUM_INTERVALS = auto()
    NUM_OUTLIERS = auto()

def sort_by_attributes(raw_result: List[AcModel], 
                       is_reverse: bool) -> List[AcModel]:
    raw_result.sort(key=json.dumps,
                    reverse=is_reverse)
    return raw_result

def sort_by_intervals(raw_result: List[AcModel], 
                      is_reverse: bool) -> List[AcModel]:
    raw_result.sort(key=lambda x: len(x['intervals']),
                    reverse=is_reverse)
    return raw_result

def sort_by_outliers(raw_result: List[AcModel], 
                      is_reverse: bool) -> List[AcModel]:
    raw_result.sort(key=lambda x: len(x['outliers']),
                    reverse=is_reverse)
    return raw_result




class AcSorter(BaseSorter):
    _sorter_map = {
        AcSortOptions.ATTRUBITES_NAMES: sort_by_attributes,   
        AcSortOptions.NUM_INTERVALS: sort_by_intervals,
        AcSortOptions.NUM_OUTLIERS: sort_by_outliers
        }

    def match_sorter_by_option_name(self, option_name):
        if sorter_option := self._sorter_map.get(option_name):
            return sorter_option
        assert_never(sorter_option)

    def sort(self, 
               raw_result: List[AcModel],
               sort_option: AcSortOptions, 
               sort_direction: SortOrder) -> List[AcModel]:

        is_reverse = sort_direction == SortOrder.DESC 
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(raw_result, is_reverse=is_reverse)
        return sorted_result

