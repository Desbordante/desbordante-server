from typing import Annotated, Literal, Union

from pydantic import Field

from app.schemas import BaseSchema

from .algo_name import NarAlgoName

# DIFFERENTIAL_STRATEGY = "DES mutation strategy to use"
SEED = "RNG seed"
MIN_CONF = "Minimum confidence value (between 0 and 1)"
MIN_SUP = "Minimum support value (between 0 and 1)"
POPULATION_SIZE = "The number of individuals in the population at any given time"
MAX_FITNESS_EVALUATIONS = "The algorithm will be stopped after calculating the fitness function this many times"
DIFFERENTIAL_SCALE = "The magnitude of mutations"
CROSSOVER_PROBABILITY = "Probability of a gene getting mutated in a new individual"


class DESConfig(BaseSchema):
    algo_name: Literal[NarAlgoName.DES]
    # differential_strategy: Literal['rand1Bin'] = Field(
    #     ..., description=DIFFERENTIAL_STRATEGY
    # )
    seed: int = Field(0, ge=0, description=SEED)
    minconf: float = Field(..., ge=0, le=1, description=MIN_CONF)
    minsup: float = Field(..., ge=0, le=1, description=MIN_SUP)
    population_size: int = Field(..., gt=0, description=POPULATION_SIZE)
    max_fitness_evaluations: int = Field(..., ge=0, description=MAX_FITNESS_EVALUATIONS)
    differential_scale: float = Field(..., gt=0, description=DIFFERENTIAL_SCALE)
    crossover_probability: float = Field(..., ge=0, le=1, description=MIN_CONF)


OneOfNarAlgoConfig = Annotated[
    Union[DESConfig],
    Field(discriminator="algo_name"),
]
