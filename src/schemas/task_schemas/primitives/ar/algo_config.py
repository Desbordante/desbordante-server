from typing import Annotated, Literal

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import ArAlgoName


class AprioriConfig(BaseSchema):
    algo_name: Literal[ArAlgoName.Apriori]
    minconf: float | None = Field(
        default=None, ge=0, le=1, description="Minimum confidence"
    )
    minsup: float | None = Field(
        default=None, ge=0, le=1, description="Minimum support"
    )


OneOfArAlgoConfig = Annotated[
    AprioriConfig,
    Field(discriminator="algo_name"),
]
