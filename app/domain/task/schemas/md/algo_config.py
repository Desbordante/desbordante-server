from typing import Annotated, Literal, Union, Optional

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import MdAlgoName

from .column_matches import ColumnMatchMetrics

#from desbordante.md.column_matches import *

#  """
#     Options:
#     right_table: second table processed by the algorithm
#     left_table: first table processed by the algorithm
#     min_support: minimum support for a dependency's LHS
#     column_matches: column matches to examine
#     level_definition: MD lattice level definition to use
#     [cardinality|lattice]
#     prune_nondisjoint: don't search for dependencies where the LHS decision boundary at the same index as the RHS decision boundary limits the number of records matched
#     max_cardinality: maximum number of MD matching classifiers
#     threads: number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently.
# """

MIN_SUPPORT = "Minimum support for a dependency's LHS"
COLUMN_MATCHES = "Column matches to examine"
LEVEL_DEFINITION = "MD lattice level definition to use"
PRUNE_NONDISJOINT = "Don't search for dependencies where the LHS decision boundary at the same index as the RHS decision boundary limits the number of records matched"
MAX_CARDINALITY = "Maximum number of MD matching classifiers"
THREADS = "Number of threads to use. If 0, then as many threads are used as the hardware can handle concurrently"


class BaseColumnMatch(BaseSchema):
    left_column: str
    right_column: str

class FullColumnMatch(BaseColumnMatch):
    minimum_similarity: float = 0.7
    bound_number_limit: int = 0

class EqualityConfig(BaseColumnMatch):
    metrics: Literal[ColumnMatchMetrics.Equality]

class JaccardConfig(FullColumnMatch):
    metrics: Literal[ColumnMatchMetrics.Jaccard]

class LevenshteinConfig(FullColumnMatch):
    metrics: Literal[ColumnMatchMetrics.Levenshtein]

class MongeElkanConfig(FullColumnMatch):
    metrics: Literal[ColumnMatchMetrics.MongeElkan]

class LcsConfig(FullColumnMatch):
    metrics: Literal[ColumnMatchMetrics.Lcs]

class LVNormNumberDistanceConfig(FullColumnMatch):
    metrics: Literal[ColumnMatchMetrics.LVNormNumberDistance]

class LVNormDateDistanceConfig(FullColumnMatch):
    metrics: Literal[ColumnMatchMetrics.LVNormDateDistance]

OneOfColumnMatchesConfig = Annotated[
    Union[LcsConfig, 
          LevenshteinConfig, 
          MongeElkanConfig, 
          EqualityConfig, 
          LVNormDateDistanceConfig, 
          LVNormNumberDistanceConfig, 
          JaccardConfig],
    Field(discriminator="metrics", description=COLUMN_MATCHES),
]


class HyMDConfig(BaseSchema):
    algo_name: Literal[MdAlgoName.HyMD]
    min_support: int = Field(1, ge=1, description=MIN_SUPPORT)
    column_matches: list[OneOfColumnMatchesConfig]
    level_definition: Literal['cardinality', 'lattice'] = Field('cardinality', description=LEVEL_DEFINITION)
    prune_nondisjoint: bool = Field(True, description=PRUNE_NONDISJOINT)
    max_cardinality: int = Field(-1, description=MAX_CARDINALITY)
    threads: int = Field(0, ge=0, le=65536, description=THREADS)


OneOfMdAlgoConfig = Annotated[
    Union[HyMDConfig],
    Field(discriminator="algo_name"),
]
