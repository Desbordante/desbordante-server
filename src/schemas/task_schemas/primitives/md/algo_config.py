from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import MdAlgoName
from .types import ColumnMatchMetric

MIN_SUPPORT = "Minimum support for a dependency's LHS"
COLUMN_MATCHES = "Column matches to examine"
LEVEL_DEFINITION = "MD lattice level definition to use"
PRUNE_NONDISJOINT = "Don't search for dependencies where the LHS decision boundary at the same index as the RHS decision boundary limits the number of records matched"
MAX_CARDINALITY = "Maximum number of MD matching classifiers"
THREADS = "Number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently"


class BaseColumnMatch(BaseSchema):
    left_column: int
    right_column: int


class FullColumnMatch(BaseColumnMatch):
    minimum_similarity: float = 0.7
    bound_number_limit: int = 0


class EqualityConfig(BaseColumnMatch):
    metric: Literal[ColumnMatchMetric.Equality]


class JaccardConfig(FullColumnMatch):
    metric: Literal[ColumnMatchMetric.Jaccard]


class LevenshteinConfig(FullColumnMatch):
    metric: Literal[ColumnMatchMetric.Levenshtein]


class MongeElkanConfig(FullColumnMatch):
    metric: Literal[ColumnMatchMetric.Monge_Elkan]


class LcsConfig(FullColumnMatch):
    metric: Literal[ColumnMatchMetric.Lcs]


class LVNormNumberDistanceConfig(FullColumnMatch):
    metric: Literal[ColumnMatchMetric.Number_Difference]


class LVNormDateDistanceConfig(FullColumnMatch):
    metric: Literal[ColumnMatchMetric.Date_Difference]


OneOfColumnMatchesConfig = Annotated[
    Union[
        LcsConfig,
        LevenshteinConfig,
        MongeElkanConfig,
        EqualityConfig,
        LVNormDateDistanceConfig,
        LVNormNumberDistanceConfig,
        JaccardConfig,
    ],
    Field(discriminator="metric", description=COLUMN_MATCHES),
]


class HyMDConfig(BaseSchema):
    algo_name: Literal[MdAlgoName.HyMD]
    min_support: int | None = Field(default=None, ge=0, description=MIN_SUPPORT)
    column_matches: list[OneOfColumnMatchesConfig]
    level_definition: Literal["cardinality", "lattice"] = Field(
        default="cardinality", description=LEVEL_DEFINITION
    )
    prune_nondisjoint: bool | None = Field(default=None, description=PRUNE_NONDISJOINT)
    max_cardinality: int | None = Field(default=None, description=MAX_CARDINALITY)
    # threads: int = Field(0, ge=0, le=65536, description=THREADS)


OneOfMdAlgoConfig = Annotated[
    Union[HyMDConfig],
    Field(discriminator="algo_name"),
]
