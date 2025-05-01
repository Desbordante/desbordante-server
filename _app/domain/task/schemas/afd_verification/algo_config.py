from typing import Annotated, Literal, Union

from pydantic import Field

from _app.schemas import BaseSchema

from .algo_name import AfdVerificationAlgoName

LHS_INDICES = "LHS column indices"
RHS_INDICES = "RHS column indices"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"


class FDVerifierConfig(BaseSchema):
    algo_name: Literal[AfdVerificationAlgoName.FDVerifier]
    lhs_indices: list[int] = Field(..., description=LHS_INDICES)
    rhs_indices: list[int] = Field(..., description=RHS_INDICES)
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


OneOfAfdVerificationAlgoConfig = Annotated[
    Union[FDVerifierConfig,],
    Field(discriminator="algo_name"),
]
