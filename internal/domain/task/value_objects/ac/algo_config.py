from typing import Literal, Annotated
from pydantic import Field
from internal.domain.common import OptionalModel
from internal.domain.task.value_objects.ac.algo_name import AcAlgoName
from internal.domain.task.value_objects.ac.algo_descriptions import descriptions


class BaseAcConfig(OptionalModel):
    __non_optional_fields__ = {
        "algo_name",
    }


class DefaultAcConfig(BaseAcConfig):
    algo_name: Literal[AcAlgoName.Default]

    bin_operation: Annotated[str, Field(description=descriptions["bin_operation"])]
    fuzziness: Annotated[
        float, Field(ge=0.1, le=1.0, description=descriptions["fuzziness"])
    ]
    p_fuzz: Annotated[float, Field(ge=0.1, le=1.0, description=descriptions["p_fuzz"])]
    weight: Annotated[float, Field(ge=0.1, le=1.0, description=descriptions["weight"])]
    bumps_limit: Annotated[int, Field(ge=0, description=descriptions["bumps_limit"])]
    iterations_limit: Annotated[
        int, Field(ge=1, description=descriptions["iterations_limit"])
    ]
    ac_seed: Annotated[int, Field(description=descriptions["ac_seed"])]


OneOfAcAlgoConfig = Annotated[
    DefaultAcConfig,
    Field(discriminator="algo_name"),
]
