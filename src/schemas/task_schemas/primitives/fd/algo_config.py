from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import FdAlgoName

# Common descriptions
MAX_LHS_DESC = "Maximum considered LHS size"
THREADS_DESC = "Number of threads to use. If 0, uses maximum available threads"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"
ERROR_DESC = "Error threshold value for Approximate FD algorithms"

# Specific descriptions
CUSTOM_SEED_DESC = (
    "Seed for custom random generator for consistent results across platforms"
)
PFD_ERROR_DESC = "PFD error measure to use"
# AFD_ERROR_DESC = "AFD error measure to use"
SEED_DESC = "RNG seed"


class BaseFdConfig(BaseSchema):
    max_lhs: int | None = Field(default=None, ge=0, description=MAX_LHS_DESC)


class AidConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.AID]


class DFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.DFD]
    # threads: int = Field(default=0, ge=0, le=8, description=THREADS_DESC)
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class DepminerConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.DEPMINER]
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class EulerFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.EULER_FD]
    custom_random_seed: int = Field(default=0, description=CUSTOM_SEED_DESC)
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class FDepConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FDEP]


class FUNConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FUN]
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class FastFDsConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FAST_FDS]
    # threads: int = Field(default=0, ge=0, description=THREADS_DESC)
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class FdMineConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.FD_MINE]
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class HyFDConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.HY_FD]
    # threads: int = Field(default=0, ge=0, description=THREADS_DESC)
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


class PyroConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.PYRO]
    # threads: int = Field(default=0, ge=0, description=THREADS_DESC)
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)
    seed: int = Field(default=0, description=SEED_DESC)


class TaneConfig(BaseFdConfig):
    algo_name: Literal[FdAlgoName.TANE]
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)


# class PFDTaneConfig(BaseFdConfig):
#     algo_name: Literal[FdAlgoName.PFD_TANE]
#     error: float = Field(default=0, ge=0, le=1, description=ERROR_DESC)
#     is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)
#     pfd_error_measure: Literal["per_tuple", "per_value"] = Field(
#         default="per_tuple", description=PFD_ERROR_DESC
#     )


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
        # PFDTaneConfig,
    ],
    Field(discriminator="algo_name"),
]
