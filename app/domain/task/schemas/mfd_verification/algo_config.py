from typing import Annotated, Literal, Union

from pydantic import Field

from app.domain.task.schemas.mfd_verification.metrics import (
    MFDVerificationMetricAlgorithm,
    MFDVerificationMetrics,
)
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
    metric_algorithm: MFDVerificationMetricAlgorithm = Field(
        ..., description=METRIC_ALGORITHM
    )


class MFDVerificationEuclideanConfig(BaseMfdVerificationConfig):
    metric: Literal[MFDVerificationMetrics.Euclidean] = Field(..., description=METRIC)


class MFDVerificationCosineConfig(BaseMfdVerificationConfig):
    metric: Literal[MFDVerificationMetrics.Cosine] = Field(..., description=METRIC)
    q: float = Field(1, ge=0, description=Q)


class MFDVerificationLevenshteinConfig(BaseMfdVerificationConfig):
    metric: Literal[MFDVerificationMetrics.Levenshtein] = Field(..., description=METRIC)


OneOfMfdVerificationAlgoConfig = Annotated[
    Union[
        MFDVerificationEuclideanConfig,
        MFDVerificationCosineConfig,
        MFDVerificationLevenshteinConfig,
    ],
    Field(discriminator="metric"),
]
