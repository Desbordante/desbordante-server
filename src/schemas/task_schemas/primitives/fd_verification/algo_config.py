from typing import Annotated, Literal

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import FdVerificationAlgoName

LHS_INDICES = "LHS column indices"
RHS_INDICES = "RHS column indices"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"


class FdVerifierConfig(BaseSchema):
    algo_name: Literal[FdVerificationAlgoName.FdVerifier]
    lhs_indices: list[int] = Field(default=[0], description=LHS_INDICES)
    rhs_indices: list[int] = Field(default=[1], description=RHS_INDICES)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


OneOfFdVerificationAlgoConfig = Annotated[
    FdVerifierConfig,
    Field(discriminator="algo_name"),
]
