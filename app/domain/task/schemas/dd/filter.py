from enum import StrEnum, auto
from typing import List, assert_never
from .task import DdModel
from app.domain.task.schemas.base import BaseFilter


class DdFilterOptions(StrEnum):
    ATTRIBUTE_NAME = auto()

def filter_by_attributes(raw_result: List[DdModel], 
                        attributes_names: List[str]) -> List[DdModel]:
    return ([
        model for model in raw_result
        if set(attributes_names).issubset(
            {sideItem['name'] for sideItem in model['lhs'] + model['rhs']})
    ])


class DdFilter(BaseFilter):
    _filter_map = {
        DdFilterOptions.ATTRIBUTE_NAME: filter_by_attributes,
    }

    def match_filter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def filter(self, 
               raw_result: List[DdModel],
               filter_option: DdFilterOptions, 
               filter_params: List[str]) -> List[DdModel]:

        filter = self.match_filter_by_option_name(filter_option)
        filtering_result = filter(raw_result, filter_params)
        return filtering_result

