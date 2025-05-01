from enum import StrEnum, auto
from typing import List, assert_never
from .task import AdcModel
from _app.domain.task.schemas.base import BaseFilter


class AdcFilterOptions(StrEnum):
    ATTRIBUTE_NAME = auto()


def filter_by_attributes(
    raw_result: List[AdcModel], attributes_names: List[str]
) -> List[AdcModel]:
    return [
        model
        for model in raw_result
        if set(attributes_names).issubset(
            {sideItem["left_item"][2::] for sideItem in model["cojuncts"]}.union(
                {sideItem["right_item"][2::] for sideItem in model["cojuncts"]}
            )
        )
    ]


class AdcFilter(BaseFilter):
    _filter_map = {
        AdcFilterOptions.ATTRIBUTE_NAME: filter_by_attributes,
    }

    def match_filter_by_option_name(self, option_name):
        if filter_option := self._filter_map.get(option_name):
            return filter_option
        assert_never(filter_option)

    def filter(
        self,
        raw_result: List[AdcModel],
        filter_option: AdcFilterOptions,
        filter_params: List[str],
    ) -> List[AdcModel]:
        filter = self.match_filter_by_option_name(filter_option)
        filtering_result = filter(raw_result, filter_params)
        return filtering_result
