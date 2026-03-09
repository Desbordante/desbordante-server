from typing import Annotated, Literal

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import AdcAlgoName

SHARD_LEHGTH = "Number of rows each shard will cover when building PLI shards. Determines the segmentation of rows for parallel processing in the FastADC algorithm"
MIN_SHARED_VALUE = (
    "Minimum threshold for the shared percentage of values between two columns"
)
COMPARABLE_THRESHOLD = "Threshold for the ratio of smaller to larger average values between two numeric columns"
ALLOW_CROSS_COLUMNS = "Specifies whether to allow the construction of Denial Constraints between different attributes"
EVIDENCE_THRESHOLD = "Denotes the maximum fraction of evidence violations allowed for a Denial Constraint to be considered approximate"


class FastAdcConfig(BaseSchema):
    algo_name: Literal[AdcAlgoName.FAST_ADC]
    shard_length: int = Field(default=0, ge=0, description=SHARD_LEHGTH)
    minimum_shared_value: int | None = Field(
        default=None, ge=0, le=1, description=MIN_SHARED_VALUE
    )
    comparable_threshold: float | None = Field(
        default=None, ge=0, le=1, description=COMPARABLE_THRESHOLD
    )
    allow_cross_columns: bool | None = Field(
        default=None, description=ALLOW_CROSS_COLUMNS
    )
    evidence_threshold: float = Field(
        default=0, ge=0, le=1, description=EVIDENCE_THRESHOLD
    )


OneOfAdcAlgoConfig = Annotated[
    FastAdcConfig,
    Field(discriminator="algo_name"),
]
