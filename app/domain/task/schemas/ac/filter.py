from enum import StrEnum, auto
from typing import List, assert_never
from .task import AcModel
from app.domain.task.schemas.base import BaseFilter


class AcFilterOptions(StrEnum):
    ATTRIBUTE_NAME = auto()


def filter_by_attributes(
    raw_result: List[AcModel], attributes_names: List[str]
) -> List[AcModel]:
    # return ([
    #    model for model in raw_result
    #     if any(attr in {model['left_column'], model['right_column']}
    #            for attr in attributes_names)
    # ])

    return [
        model
        for model in raw_result
        if set(attributes_names).issubset(
            {model["left_column"]}.union({model["right_column"]})
        )
    ]


class AcFilter(BaseFilter):
    _filter_map = {
        AcFilterOptions.ATTRIBUTE_NAME: filter_by_attributes,
    }

    def match_filter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def filter(
        self,
        raw_result: List[AcModel],
        filter_option: AcFilterOptions,
        filter_params: List[str],
    ) -> List[AcModel]:
        filter = self.match_filter_by_option_name(filter_option)
        filtering_result = filter(raw_result, filter_params)
        return filtering_result
