from typing import Annotated, Literal

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import AcAlgoName

BUMPS_LIMIT = "Max considered intervals amount. Pass 0 to remove limit"
FUZZINESS = "Fraction of exceptional records, lies in (0, 1]"
AC_SEED = "Seed, needed for choosing a data sample"
ITERATION_LIMIT = "Limit for iterations of sampling"
P_FUZZ = "Probability, the fraction of exceptional records that lie outside the bump intervals is at most Fuzziness, lies in (0, 1]"
WEIGHT = "Value lies in (0, 1]. Closer to 0 - many short intervals. Closer to 1 - small number of long intervals"
BIN_OPERATION = "one of available operations: /, *, +, -"


class BHUNTConfig(BaseSchema):
    algo_name: Literal[AcAlgoName.BHUNT]
    bumps_limit: int = Field(0, ge=0, description=BUMPS_LIMIT)
    ac_seed: int = Field(11, ge=0, description=AC_SEED)
    iterations_limit: int = Field(4, ge=1, description=ITERATION_LIMIT)
    fuzziness: float = Field(0.2, ge=0, le=1, description=FUZZINESS)
    p_fuzz: float = Field(0.85, gt=0, le=1, description=P_FUZZ)
    weight: float = Field(0.1, gt=0, le=1, description=WEIGHT)
    bin_operation: Literal["+", "-", "*", "/"] = Field("-", description=BIN_OPERATION)


OneOfAcAlgoConfig = Annotated[
    BHUNTConfig,
    Field(discriminator="algo_name"),
]
