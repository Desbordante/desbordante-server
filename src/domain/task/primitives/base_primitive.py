from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Mapping, Protocol, Sequence

import desbordante
from pydantic import TypeAdapter

from src.schemas.base_schemas import BaseSchema
from src.schemas.dataset_schemas import DatasetType, OneOfDownloadedDatasetSchema


class BaseAlgoConfig(Protocol):
    @property
    def algo_name(self) -> StrEnum: ...


class BaseParams(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    @property
    def config(self) -> BaseAlgoConfig: ...

    @property
    def datasets(self) -> BaseSchema: ...


class BasePrimitive[
    A: desbordante.Algorithm,
    N: StrEnum,
    P: BaseParams,
    C: BaseAlgoConfig,
    D: BaseSchema,
    R: Sequence[BaseSchema],
](ABC):
    _algo: A
    _algo_map: Mapping[N, type[A]]
    _params_schema_class: type[P]
    downloaded_dataset_class: type[OneOfDownloadedDatasetSchema]
    datasets_config_class: type[D]

    allowed_dataset_type: DatasetType

    @classmethod
    def validate_params(cls, params: BaseParams) -> P:
        return TypeAdapter(cls._params_schema_class).validate_python(params)

    def __init__(self, *, algo_name: N):
        self._algo = self._get_algo_by_name(algo_name)

    def _get_algo_by_name(self, algo_name: N) -> A:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        raise ValueError(f"Algorithm {algo_name} not found")

    @abstractmethod
    def execute(self, config: C, datasets: D) -> R: ...
