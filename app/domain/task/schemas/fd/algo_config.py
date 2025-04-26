from typing import Annotated, Literal, Union

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import FdAlgoName

# Common descriptions
MAX_LHS_DESC = "Maximum considered LHS size"
THREADS_DESC = "Number of threads to use. If 0, uses maximum available threads"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"
# ERROR_DESC = "Error threshold value for Approximate FD algorithms"

# Specific descriptions
CUSTOM_SEED_DESC = (
    "Seed for custom random generator for consistent results across platforms"
)
# PFD_ERROR_DESC = "PFD error measure to use"
# AFD_ERROR_DESC = "AFD error measure to use"
SEED_DESC = "RNG seed"


class BaseFdConfig(BaseSchema):
    max_lhs: int = Field(0, ge=0, description=MAX_LHS_DESC)


class AidConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Aid]


class DFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.DFD]
    threads: int = Field(0, ge=0, le=8, description=THREADS_DESC)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class DepminerConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Depminer]
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class EulerFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.EulerFD]
    custom_random_seed: int = Field(0, description=CUSTOM_SEED_DESC)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class FDepConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FDep]


class FUNConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FUN]
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class FastFDsConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FastFDs]
    threads: int = Field(0, ge=0, description=THREADS_DESC)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class FdMineConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FdMine]
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class HyFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.HyFD]
    threads: int = Field(0, ge=0, description=THREADS_DESC)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class PyroConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Pyro]
    threads: int = Field(0, ge=0, description=THREADS_DESC)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)
    seed: int = Field(0, description=SEED_DESC)


class TaneConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.Tane]
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


OneOfFdAlgoConfig = Annotated[
    Union[
        AidConfig,
        DFDConfig,
        DepminerConfig,
        EulerFDConfig,
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
