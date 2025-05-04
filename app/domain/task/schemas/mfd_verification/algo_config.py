from typing import Annotated, Literal, Union

from pydantic import Field

from app.domain.task.schemas.mfd_verification.metrics import MetricAlgorith, Metrics
from app.schemas import BaseSchema

from .algo_name import MfdVerificationAlgoName

LHS_INDICES = "LHS column indices"
RHS_INDICES = "RHS column indices"
PARAMETER = "Metric FD parameter"
DIST_FROM_NULL_IS_INFINITY = "Specify whether distance from NULL value is infinity"
NULL_EQUAL_DESC = "Whether two NULL values should be considered equal"

METRIC = ""
METRIC_ALGORITHM = ""
Q = ""


class BaseMfdVerificationConfig(BaseSchema):
    algo_name: Literal[MfdVerificationAlgoName.MetricVerification]
    lhs_indices: list[int] = Field(..., description=LHS_INDICES)
    rhs_indices: list[int] = Field(..., description=RHS_INDICES)
    parameter: float = Field(1, ge=0, description="Parameter for the metric algorithm")
    dist_from_null_is_infinity: bool = Field(
        False,
        description=DIST_FROM_NULL_IS_INFINITY,
    )
    is_null_equal_null: bool = Field(False, description=NULL_EQUAL_DESC)


class EuclideanConfig(BaseMfdVerificationConfig):
    metric: Literal[Metrics.Euclidean] = Field(..., description=METRIC)
    metric_algorithm: Literal[
        MetricAlgorith.Brute, MetricAlgorith.Approx, MetricAlgorith.Calipers
    ] = Field(..., description=METRIC_ALGORITHM)


class CosineConfig(BaseMfdVerificationConfig):
    metric: Literal[Metrics.Cosine] = Field(..., description=METRIC)
    metric_algorithm: Literal[MetricAlgorith.Brute, MetricAlgorith.Approx] = Field(
        ..., description=METRIC_ALGORITHM
    )
    q: float = Field(1, ge=0, description=Q)


class LevenshteinConfig(BaseMfdVerificationConfig):
    metric: Literal[Metrics.Levenshtein] = Field(..., description=METRIC)
    metric_algorithm: Literal[MetricAlgorith.Brute, MetricAlgorith.Approx] = Field(
        ..., description=METRIC_ALGORITHM
    )


OneOfMfdVerificationAlgoConfig = Annotated[
    Union[
        EuclideanConfig,
        CosineConfig,
        LevenshteinConfig,
    ],
    Field(discriminator="metric"),
]
