from typing import Annotated, Literal, Union

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import ARAlgoName


class AprioriConfig(BaseSchema):
    algo_name: Literal[ARAlgoName.AssosiatioRulesApriori]
    input_format: Literal["tabular", "singular"] = Field(
        "tabular", description="Input format"
    )
    minconf: float = Field(0, ge=0, le=1, description="Minimum confidence")
    minsup: float = Field(0, ge=0, le=1, description="Minimum support")


OneOfARAlgoConfig = Annotated[
    Union[AprioriConfig],
    Field(discriminator="algo_name"),
]
