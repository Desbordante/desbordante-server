from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Mapping, Protocol

from desbordante import Algorithm
from pydantic import TypeAdapter

from src.schemas.base_schemas import BaseSchema
from src.schemas.dataset_schemas import DatasetType


class BaseAlgoConfig(Protocol):
    @property
    def algo_name(self) -> StrEnum: ...

    def model_dump(
        self,
        *,
        exclude: set[str] | None = None,
        exclude_unset: bool = False,
    ) -> dict[str, Any]: ...


class BaseParams(Protocol):
    @property
    def primitive_name(self) -> StrEnum: ...

    @property
    def config(self) -> BaseAlgoConfig: ...

    @property
    def datasets(self) -> BaseSchema: ...


class BasePrimitive[
    A: Algorithm,
    N: StrEnum,
    P: BaseParams,
    R: BaseSchema,
](ABC):
    _algo: A
    _algo_map: Mapping[N, type[A]]
    _params_schema_class: type[P]
    allowed_dataset_type: DatasetType

    @classmethod
    def validate_params(cls, params: Any) -> P:
        return TypeAdapter(cls._params_schema_class).validate_python(params)

    def __init__(self, *, algo_name: N):
        self._algo = self._get_algo_by_name(algo_name)

    def _get_algo_by_name(self, algo_name: N) -> A:
        if algo_class := self._algo_map.get(algo_name):
            return algo_class()
        raise ValueError(f"Algorithm {algo_name} not found")

    def _get_algo_options(self, params: P) -> dict[str, Any]:
        return params.config.model_dump(exclude_unset=True, exclude={"algo_name"})

    @abstractmethod
    def execute(self, params: P) -> list[R]: ...
