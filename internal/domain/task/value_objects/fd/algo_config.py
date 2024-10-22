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

    max_lhs: Annotated[int, Field(ge=1, le=10)]


class DFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.DFD]

    max_lhs: Annotated[int, Field(ge=1, le=10)]
    is_null_equal_null: bool
    threads: Annotated[int, Field(ge=1, le=8)]


class DepminerConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Depminer]

    max_lhs: Annotated[int, Field(ge=1, le=10)]
    is_null_equal_null: bool


class FDepConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FDep]

    max_lhs: Annotated[int, Field(ge=1, le=10)]


class FUNConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FUN]

    max_lhs: Annotated[int, Field(ge=1, le=10)]
    is_null_equal_null: bool


class FastFDsConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FastFDs]

    is_null_equal_null: bool
    max_lhs: Annotated[int, Field(ge=1, le=10)]
    threads: Annotated[int, Field(ge=1, le=8)]


class FdMineConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FdMine]

    max_lhs: Annotated[int, Field(ge=1, le=10)]
    is_null_equal_null: bool


class HyFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.HyFD]

    max_lhs: Annotated[int, Field(ge=1, le=10)]
    is_null_equal_null: bool


class PFDTaneConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.PFDTane]

    is_null_equal_null: bool
    error: Annotated[float, Field(ge=0, le=1)]
    error_measure: Annotated[str, Literal["per_tuple", "per_value"]]
    max_lhs: Annotated[int, Field(ge=1, le=10)]


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
        PFDTaneConfig,
        PyroConfig,
        TaneConfig,
    ],
    Field(discriminator="algo_name"),
]
