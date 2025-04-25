from enum import StrEnum, auto
from typing import List, assert_never
from .task import NarModel
from _app.domain.task.schemas.base import BaseSorter
from _app.domain.task.schemas.types import SortOrder
import json


class NarSortOptions(StrEnum):
    LHS = auto()
    RHS = auto()

def sort_by_lhs(raw_result: List[NarModel], 
                is_reverse: bool) -> List[NarModel]:
    raw_result.sort(key=json.dumps,
                           reverse=is_reverse)
    return raw_result

def sort_by_rhs(raw_result: List[NarModel], 
                is_reverse: bool) -> List[NarModel]:
    raw_result.sort(key=lambda x: json.dumps({'rhs': x['rhs'], 
                                                     'lhs': x['lhs']}),
                           reverse=is_reverse)
    return raw_result




class NarSorter(BaseSorter):
    _filter_map = {
        NarSortOptions.LHS: sort_by_lhs,   
        NarSortOptions.RHS: sort_by_rhs,  }

    def match_sorter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def sort(self, 
               raw_result: List[NarModel],
               sort_option: NarSortOptions, 
               sort_direction: SortOrder) -> List[NarModel]:

        is_reverse = sort_direction == SortOrder.DESC 
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(raw_result, is_reverse=is_reverse)
        return sorted_result

