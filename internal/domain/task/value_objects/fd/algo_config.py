from typing import Literal, Annotated, Union

from pydantic import Field

from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.fd.algo_name import FdAlgoName


class BaseFdConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class AidConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Aid]

    is_null_equal_null: bool


class DFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.DFD]

    is_null_equal_null: bool
    threads: Annotated[int, Field(ge=1, le=8)]


class DepminerConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Depminer]

    is_null_equal_null: bool


class FDepConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FDep]

    is_null_equal_null: bool


class FUNConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FUN]

    is_null_equal_null: bool


class FastFDsConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FastFDs]

    is_null_equal_null: bool
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]


class FdMineConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FdMine]

    is_null_equal_null: bool


class HyFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.HyFD]

    is_null_equal_null: bool


class PyroConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Pyro]

    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]
    seed: int


class TaneConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Tane]

    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    max_lhs: Annotated[int, Field(ge=1, le=10)]


OneOfFdAlgoConfig = Annotated[
    Union[
        AidConfig,
        DFDConfig,
        DepminerConfig,
        FDepConfig,
        FUNConfig,
        FastFDsConfig,
        FdMineConfig,
        HyFDConfig,
        PyroConfig,
        TaneConfig,
    ],
    Field(discriminator="algo_name"),
]
