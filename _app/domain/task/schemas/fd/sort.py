from enum import StrEnum, auto
from typing import List, assert_never
from .task import FdModel
from _app.domain.task.schemas.base import BaseSorter
from _app.domain.task.schemas.types import SortOrder
import json


class FdSortOptions(StrEnum):
    LHS = auto()
    RHS = auto()

def sort_by_lhs(raw_result: List[FdModel], 
                is_reverse: bool) -> List[FdModel]:
    raw_result.sort(key=json.dumps,
                           reverse=is_reverse)
    return raw_result

def sort_by_rhs(raw_result: List[FdModel], 
                is_reverse: bool) -> List[FdModel]:
    raw_result.sort(key=lambda x: json.dumps({'rhs': x['rhs'], 
                                                     'lhs': x['lhs']}),
                           reverse=is_reverse)
    return raw_result




class FdSorter(BaseSorter):
    _sorter_map = {
        FdSortOptions.LHS: sort_by_lhs,   
        FdSortOptions.RHS: sort_by_rhs,  }

    def match_sorter_by_option_name(self, option_name):
        if sorter_option := self._sorter_map.get(option_name):
            return sorter_option
        assert_never(sorter_option)

    def sort(self, 
               raw_result: List[FdModel],
               sort_option: FdSortOptions, 
               sort_direction: SortOrder) -> List[FdModel]:

        is_reverse = sort_direction == SortOrder.DESC 
        sorter = self.match_sorter_by_option_name(sort_option)
        sorted_result = sorter(raw_result, is_reverse=is_reverse)
        return sorted_result

