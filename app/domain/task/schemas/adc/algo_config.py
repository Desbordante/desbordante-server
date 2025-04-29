from typing import Annotated, Literal, Union

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import AdcAlgoName

SHARD_LEHGTH = 'Number of rows each shard will cover when building PLI shards. Determines the segmentation of rows for parallel processing in the FastADC algorithm'
MIN_SHARD_VALUE = 'Minimum threshold for the shared percentage of values between two columns'
COMPARABLE_THRESHOLD = 'Threshold for the ratio of smaller to larger average values between two numeric columns'
ALLOW_CROSS_COLUMNS = 'Specifies whether to allow the construction of Denial Constraints between different attributes'
EVIDENCE_THRESHOLD = 'Denotes the maximum fraction of evidence violations allowed for a Denial Constraint to be considered approximate'

class FastADCConfig(BaseSchema):
    algo_name: Literal[AdcAlgoName.FastADC]
    shard_length: int = Field(0, ge=0, description=MIN_SHARD_VALUE)
    minimum_shared_value: int = Field(0, ge=0, description=MIN_SHARD_VALUE)
    comparable_threshold: float = Field(0, ge=0, le=1, description=COMPARABLE_THRESHOLD)
    allow_cross_columns: bool = Field(True, description=ALLOW_CROSS_COLUMNS)
    evidence_threshold: float = Field(0, ge=0, le=1, description=EVIDENCE_THRESHOLD)


OneOfAdcAlgoConfig = Annotated[
    Union[FastADCConfig],
    Field(discriminator="algo_name"),
]
