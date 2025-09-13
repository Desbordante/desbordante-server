from typing import Annotated, Literal, Union

from pydantic import Field

from src.schemas.base_schemas import BaseSchema

from .algo_name import NarAlgoName

DIFFERENTIAL_STRATEGY = "DES mutation strategy to use"
SEED = "RNG seed"
MIN_CONF = "Minimum confidence value (between 0 and 1)"
MIN_SUP = "Minimum support value (between 0 and 1)"
POPULATION_SIZE = "The number of individuals in the population at any given time"
MAX_FITNESS_EVALUATIONS = "The algorithm will be stopped after calculating the fitness function this many times"
DIFFERENTIAL_SCALE = "The magnitude of mutations"
CROSSOVER_PROBABILITY = "Probability of a gene getting mutated in a new individual"


class DesConfig(BaseSchema):
    algo_name: Literal[NarAlgoName.DES]
    # differential_strategy: DifferentialStrategy = Field(
    #     ..., description=DIFFERENTIAL_STRATEGY
    # )
    seed: int | None = Field(None, ge=0, description=SEED)
    minconf: float = Field(default=0.7, ge=0, le=1, description=MIN_CONF)
    minsup: float = Field(default=0.1, ge=0, le=1, description=MIN_SUP)
    population_size: int = Field(default=500, gt=0, description=POPULATION_SIZE)
    max_fitness_evaluations: int = Field(
        default=700, ge=0, description=MAX_FITNESS_EVALUATIONS
    )
    differential_scale: float | None = Field(
        default=None, gt=0, description=DIFFERENTIAL_SCALE
    )
    crossover_probability: float | None = Field(
        default=None, ge=0, le=1, description=CROSSOVER_PROBABILITY
    )


OneOfNarAlgoConfig = Annotated[
    Union[DesConfig],
    Field(discriminator="algo_name"),
]
