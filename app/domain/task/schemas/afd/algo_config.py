from typing import Annotated, Literal, Union

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import AfdAlgoName

# Common descriptions
MAX_LHS_DESC = "Maximum considered LHS size"
THREADS_DESC = "Number of threads to use. If 0, uses maximum available threads"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"
ERROR_DESC = "Error threshold value for Approximate FD algorithms"

# Specific descriptions
AFD_ERROR_DESC = "AFD error measure to use"
SEED_DESC = "RNG seed"


class BaseAfdConfig(BaseSchema):
    max_lhs: int = Field(0, ge=0, description=MAX_LHS_DESC)
    error: float = Field(0, ge=0, le=1, description=ERROR_DESC)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)

class AFDPyroConfig(BaseAfdConfig):
    algo_name: Literal[AfdAlgoName.Pyro]
    threads: int = Field(0, ge=0, description=THREADS_DESC)
    seed: int = Field(0, description=SEED_DESC)


class AFDTaneConfig(BaseAfdConfig):
    algo_name: Literal[AfdAlgoName.Tane]
    afd_error_measure: Literal["g1", "pdep", "tau", "mu_plus", "rho"] = Field(
        "g1", description=AFD_ERROR_DESC
    )


OneOfAfdAlgoConfig = Annotated[
    Union[
        AFDPyroConfig,
        AFDTaneConfig,
    ],
    Field(discriminator="algo_name"),
]
