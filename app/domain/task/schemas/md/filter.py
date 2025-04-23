from enum import StrEnum, auto
from typing import List, assert_never
from .task import MdModel
from .column_matches import ColumnMatchMetrics
from app.domain.task.schemas.base import BaseFilter

class MdFilterOptions(StrEnum):
    ATTRIBUTE_NAME = auto()
    METRICS = auto()


def filter_by_attributes(raw_result: List[MdModel], 
                        attributes_names: List[str]) -> List[MdModel]:
    attributes_set = set(attributes_names)
    filtered_models = []
    for model in raw_result:
        all_columns = set()
        for sideItem in model['lhs'] + model['rhs']:
            all_columns.add(sideItem['left_column'])
            all_columns.add(sideItem['right_column'])
        
        if attributes_set.issubset(all_columns):
            filtered_models.append(model)
    
    print(filtered_models)

    return (filtered_models)

def filter_by_metrics(raw_result: List[MdModel], 
                     metrics: List[ColumnMatchMetrics]) -> List[MdModel]:
    return ([
        model for model in raw_result
        if set(metrics).issubset(
            {sideItem['metrics'] for sideItem in model['lhs'] + model['rhs']})
    ])



class MdFilter(BaseFilter):
    _filter_map = {
        MdFilterOptions.ATTRIBUTE_NAME: filter_by_attributes,
        MdFilterOptions.METRICS: filter_by_metrics,
    }

    def match_filter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def filter(self, 
               raw_result: List[MdModel],
               filter_option: MdFilterOptions, 
               filter_params: List[str]) -> List[MdModel]:

        filter = self.match_filter_by_option_name(filter_option)
        filtering_result = filter(raw_result, filter_params)
        return filtering_result

