from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import PfdAlgoName

MAX_LHS_DESC = "Maximum considered LHS size"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"
ERROR_DESC = "Error threshold value for Approximate FD algorithms"
PFD_ERROR_DESC = "PFD error measure to use"


class PfdTaneConfig(BaseSchema):
    algo_name: Literal[PfdAlgoName.PFDTane]
    max_lhs: int | None = Field(default=None, ge=0, description=MAX_LHS_DESC)
    error: float = Field(default=0, ge=0, le=1, description=ERROR_DESC)
    is_null_equal_null: bool | None = Field(default=None, description=NULL_EQUAL_DESC)
    pfd_error_measure: Literal["per_tuple", "per_value"] = Field(
        default="per_tuple", description=PFD_ERROR_DESC
    )


OneOfPfdAlgoConfig = Annotated[
    Union[PfdTaneConfig,],
    Field(discriminator="algo_name"),
]
